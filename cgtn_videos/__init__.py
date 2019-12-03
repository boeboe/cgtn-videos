"""Package to retreive CGTN videos """
from os.path import dirname, basename, isfile
import glob

from .category import Category, CategoryParser
from .config import REQUEST_TIMEOUT
from .livestream import Livestream, LivestreamParser
from .program import ProgramVideo, ProgramParser
from .region import Region
from .section import SectionVideo, SectionParser, SectionFR, SectionAR, SectionSP, SectionRU
from .special import Special, SpecialParser
from .video import Video, VideoParser

__version__ = '0.0.1'

MODULES = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in MODULES if isfile(f) and not f.endswith('__init__.py')]
