"""Package to retreive CGTN videos """
from os.path import dirname, basename, isfile
import glob

from .category import Category, CategoryParser
from .channel import ChannelProgram, ChannelParser, Channel
from .config import REQUEST_TIMEOUT
from .program import ProgramVideo, ProgramParser
from .section import SectionVideo, SectionParser, SectionFR, SectionAR, SectionSP, SectionRU
from .special import Special, SpecialParser
from .video import Video, VideoParser

__version__ = '0.0.2'

MODULES = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in MODULES if isfile(f) and not f.endswith('__init__.py')]
