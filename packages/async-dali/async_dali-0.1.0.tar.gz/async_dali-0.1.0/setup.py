import setuptools

setuptools.setup(
    name="async_dali",
    version="0.1.0",
    author="Bruce Cooper",
    description="A module to discover devices and send commands to DALI enabled lights",
    url="https://github.com/brucejcooper/py_async_dali",
    packages=["async_dali"],
    license="MIT",
    install_requires=["hid", "dom_query", "dateparser"]
)