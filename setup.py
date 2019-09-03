import setuptools
from textnorm import __version__

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="textnorm",
  version=__version__,
  description="Text Normalizer",
  url="https://github.com/kkorovesis/textnorm",
  packages=setuptools.find_packages(),

  classifiers=[
    "Programming Language :: Python :: 2.7",
    "Operating System :: Unix Based",
  ],
)