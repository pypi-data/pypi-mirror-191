
import asyncio
import logging
import struct
import threading
import traceback
from enum import Enum

import hid

from .bus_transciever import (AddressedCommand, BadFrame, BroadcastCommand,
                              DaliBusTransciever, DirectArcPowerCommand,
                              NakMessage, NumericResponseMessage,
                              SpecialCommand)
from .types import (DaliCommandCode, DaliCommandType, DaliException,
                    FramingException, MessageSource, SpecialCommandCode)

_LOGGER = logging.getLogger(__name__)


class MessageType(Enum):
    NAK = 0x71
    RESPONSE = 0x72
    TX_COMPLETE = 0x73
    BROADCAST_RECEIVED = 0x74
    FRAMING_ERROR = 0x77


class TridonicDali(DaliBusTransciever):

    def __init__(self, hid, evt_loop=None) -> None:
        DaliBusTransciever.__init__(self)
        self.next_sequence = 1
        self.hid = hid

        self.outstanding_commands = dict()

        if evt_loop is None:
            self.evt_loop = asyncio.get_event_loop()
        else:
            self.evt_loop = evt_loop

        # Add a default callback handler to deal with Responses
        self._new_message_callbacks.append(self.resolve_futures)

    @classmethod
    def scan_for_transcievers(cls):
        res = []
        for dev in hid.enumerate(0x17b5, 0x0020):
            res.append(TridonicDali(hid.Device(dev['vendor_id'], dev['product_id'], dev['serial_number'])))

        return res

    def __repr__(self):
        return "<Tridonic Dali USB adapter serial={}>".format(self.hid.serial)

    async def __aenter__(self):
        self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        await self.close()

    def open(self):
        self._stop_listening = threading.Event()
        self._read_thread = threading.Thread(target=self.read_loop, daemon=True)
        self._read_thread.start()

    def read_message(self, msg):
        print("READ", msg)


    def resolve_futures(self, msg):

        future = self.outstanding_commands.get(msg.sequence_number, None)
        if future is not None:
            if isinstance(msg, NumericResponseMessage):
                future.set_result(msg.value)
                del self.outstanding_commands[msg.sequence_number]
            elif isinstance(msg, NakMessage):
                future.set_result(None)
                del self.outstanding_commands[msg.sequence_number]
            elif isinstance(msg, BadFrame):
                future.set_exception(FramingException("Framing Error"))
                del self.outstanding_commands[msg.sequence_number]

    def read_loop(self):
        while not self._stop_listening.is_set():
            try:
                ret = self.receive()
                if ret is not None:
                    for callback in self._new_message_callbacks:
                        self.evt_loop.call_soon_threadsafe(callback, ret)
            except Exception as ex:
                _LOGGER.error("Got Exception")
                traceback.print_exc()
                self.close()
        print("Reader finished")

    async def close(self):
        self._stop_listening.set()
        self.hid.close()  # This will cause any active call to read to throw an exception.
        # if self._read_thread is not None:
        #    self._read_thread.join() # This could wait up to 100ms due to the timeout nature of the reading thread.
        self.hid = None

    def get_seq(self):
        newseq = self.next_sequence
        self.next_sequence = self.next_sequence + 1  # Note: Not thread safe
        if self.next_sequence > 255:
            self.next_sequence = 1  # Sequence 0 is reserved for external entities
        return newseq

    def _send(self, cmd: int, length=16, repeat=1):
        """Data expected by DALI USB:
        dr sn rp ty ?? ec ad cm .. .. .. .. .. .. .. ..
        12 1d 00 03 00 00 ff 08 00 00 00 00 00 00 00 00

        dr: direction
            0x12 = USB side
        rp: 0x20 for repeat twice, 0x00 otherwise.
        sn: seqnum
        ty: type
            0x03 = 16bit
            0x04 = 24bit
            0x06 = DA24 Conf (???)
        ec: ecommand (first byte for 24 bit ones)
        ad: address
        cm: command


        example command for START QUIESCENT Command
        12 01 20 06 00 ff fe 1d 00 00 00 00 00 00 00 00...
        """
        response = asyncio.Future()

        if self.hid is None:
            response.set_exception(Exception("Device not open"))
            return response

        seq = self.get_seq()
        data = bytearray(64)  # Transmitted packets are 64 bytes wide, but most of them (all but the first 8) are 0x00
        data[0] = MessageSource.SELF.value  # USB side command
        data[1] = seq
        if repeat == 2:
            data[2] = 0x20

        if length == 16:
            data[3] = 0x03
        else:
            if length == 24:
                data[3] = 0x04
            elif length == 25:  # Magic value for DA24 extended command.
                data[3] = 0x06
            else:
                raise DaliException("Invalid length")
            data[5] = (cmd >> 16) & 0xFF

        data[6] = (cmd >> 8) & 0xFF
        data[7] = cmd & 0xFF
        # print("SND {} - {}".format(bytes(data), len(data)))

        self.hid.write(bytes(data))

        # To make things easier on implementers, we automatically correlate Commands and responses.
        self.outstanding_commands[seq] = response
        self.last_command = response
        return response

    def receive(self, timeout=None):
        """Raw data received from DALI USB:
        dr ty ?? ec ad cm st st sn .. .. .. .. .. .. ..
        11 73 00 00 ff 93 ff ff 00 00 00 00 00 00 00 00

        dr: direction
            0x11 = DALI side
            0x12 = USB side
        ty: type
            0x71 = transfer no response
            0x72 = transfer response
            0x73 = transfer complete
            0x74 = broadcast received (?)
            0x76 = ?
            0x77 = framing error
        ec: ecommand
        ad: address
        cm: command
            also serves as response code for 72
        st: status
            internal status code, value unknown
        sn: seqnum
        """
        if self.hid is None:
            raise Exception("Device not open")
        data = self.hid.read(16, timeout)
        if data is None or len(data) == 0:
            return None

        dr = MessageSource(data[0])
        ty = MessageType(data[1])
        ec = data[3]
        ad = data[4]
        cmd_or_response = data[5]
        st = struct.unpack('H', data[6:8])[0]
        sequence_number = data[8]

        msg = None

        try:
            if ty == MessageType.NAK:
                msg = NakMessage(self, dr, sequence_number)
            elif ty == MessageType.RESPONSE:
                msg = NumericResponseMessage(self, dr, sequence_number, cmd_or_response)
            else:
                ct = DaliCommandType.from_addr(ad)
                if ct == DaliCommandType.SPECIAL_COMMAND:
                    msg = SpecialCommand(self, dr, sequence_number, SpecialCommandCode(ad), cmd_or_response)
                elif ct == DaliCommandType.GEAR_ADDRESSED or ct == DaliCommandType.GROUP_ADDRESSED:
                    msg = AddressedCommand(self, dr, sequence_number, ad, DaliCommandCode(cmd_or_response))
                elif ct == DaliCommandType.BROADCAST:
                    msg = BroadcastCommand(self, dr, sequence_number, False, DaliCommandCode(cmd_or_response))
                elif ct == DaliCommandType.UNADDRESSED_BROADCAST:
                    msg = BroadcastCommand(self, dr, sequence_number, True, DaliCommandCode(cmd_or_response))
                elif ct == DaliCommandType.DIRECT_ARC_POWER_COMMAND:
                    msg = DirectArcPowerCommand(self, dr, sequence_number, ad, cmd_or_response)
                else:
                    raise DaliException("unknown message type")
        except:
            _LOGGER.error("Could not process {} {} {:02x} {:02x} {:02x} {} {}".format(dr, ty, ec, ad, cmd_or_response, st, sequence_number))
            traceback.print_exc()

        return msg
