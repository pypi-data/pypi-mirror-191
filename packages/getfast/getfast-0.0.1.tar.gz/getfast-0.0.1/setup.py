import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getfast",
    version="0.0.1",
    author="wd021",
    author_email="getfastdeveloper@gmail.com",
    description="Easiest way to measure the speed of your code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://getfast.dev",
    packages=setuptools.find_packages()
)
