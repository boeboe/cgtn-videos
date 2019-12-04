"""Package to retreive CGTN videos and metadata """
from os.path import dirname, basename, isfile
import glob

__version__ = '0.0.4'

MODULES = glob.glob(dirname(__file__)+"/*.py")
__all__ = [basename(f)[:-3] for f in MODULES if isfile(f) and not f.endswith('__init__.py')]
