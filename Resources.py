import pyglet

class Resources:
    """   """

    WHITE_TILE = pyglet.image.load("assets/white_tile.png")
    BLACK_TILE = pyglet.image.load("assets/black_tile.png")
    SELECTED_TILE = pyglet.image.load("assets/selected_tile.png")
    HIGHTLIGHTED_TILE = pyglet.image.load("assets/highlighted_tile.png")

    WHITE_PIECE = pyglet.image.load("assets/white_piece.png")
    BLACK_PIECE = pyglet.image.load("assets/black_piece.png")
    PROMOTED_WHITE_PIECE = pyglet.image.load("assets/promoted_white_piece.png")
    PROMOTED_BLACK_PIECE = pyglet.image.load("assets/promoted_black_piece.png")

    EMPTY = pyglet.image.load("assets/no_piece.png")
