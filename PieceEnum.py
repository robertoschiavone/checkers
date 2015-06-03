from enum import Enum, unique

@unique
class PieceEnum(Enum):
    """   """

    EMPTY = 0
    
    WHITE_PIECE = 1
    BLACK_PIECE = 2

    PROMOTED_WHITE_PIECE = 3
    PROMOTED_BLACK_PIECE = 4
