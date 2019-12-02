"""Package to represent CGTN regions """
from enum import Enum

class Region(Enum):
    """Class enum to represent CTGN regions """

    ENGLISH = 'english'
    SPANISH = 'spanish'
    FRENCH = "french"
    ARABIC = "arabic"
    RUSSIAN = "russian"
    DOCUMENTARY = "documentary"
