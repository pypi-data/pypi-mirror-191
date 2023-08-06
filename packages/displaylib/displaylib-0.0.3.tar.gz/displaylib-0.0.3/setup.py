from setuptools import setup
from displaylib import __version__, __author__


setup(
   name="displaylib",
   version=__version__,
   description="Display an ASCII world",
   author=__author__,
   packages=[
      "displaylib",
      "displaylib.template",
      "displaylib.ascii",
      "displaylib.pygame"
   ]
)
