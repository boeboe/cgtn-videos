"""Package to retreive CGTN videos """
from os.path import dirname, basename, isfile
import glob

from .livestream import Livestream, LivestreamParser
from .category import Category, CategoryParser
from .program import ProgramVideo, ProgramParser
from .region import Region

__version__ = '0.0.1'

MODULES = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in MODULES if isfile(f) and not f.endswith('__init__.py')]
