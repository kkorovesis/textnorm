import setuptools
from xnorm import __version__

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="xnorm",
  version=__version__,
  description="Generic Text Normalizer",
  url="https://bitbucket.org/xplainlabs/xnorm",
  packages=setuptools.find_packages(),

  classifiers=[
    "Programming Language :: Python :: 2.7",
    "Operating System :: Unix Based",
  ],
)