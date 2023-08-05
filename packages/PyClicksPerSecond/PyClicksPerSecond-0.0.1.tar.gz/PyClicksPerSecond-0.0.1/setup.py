from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Measuring your clicks per second'
LONG_DESCRIPTION = 'A package that allows you to Measure how fast you click also known as clicks per second or cps.'

# Setting up
setup(
    name="PyClicksPerSecond",
    version=VERSION,
    author="Computer4062 (Mihan)",
    author_email="mihan.edirisinghe@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cps', 'clicks', 'mouse', 'gamming'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
