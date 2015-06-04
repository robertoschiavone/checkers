"""
"""
#
# The MIT License (MIT)
#
# Copyright (c) 2015, Roberto Schiavone
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from PieceEnum import *
from Resources import *

import pyglet

class Checkerboard:

    background = None

    pieces = None

    gfx_pieces = None

    @staticmethod
    def initialize_background(width, height, batch):
        """Alterna le caselle bianche e nere nella grafica dello sfondo e 
        restituisce la matrice degli Sprite"""
        
        Checkerboard.background = [[None for x in range(height)] for x in range(width)]

        for x in range(width):
            for y in range(height):
                if (x + y) % 2 == 0:
                    Checkerboard.background[x][y] = pyglet.sprite.Sprite(Resources.WHITE_TILE)
                else:
                    Checkerboard.background[x][y] = pyglet.sprite.Sprite(Resources.BLACK_TILE)

                Checkerboard.background[x][y].batch = batch
                Checkerboard.background[x][y].position = (x * 64, y * 64)

    @staticmethod
    def initialize_pieces(width, height, batch):
        
        Checkerboard._initialize_logic(width, height)

        Checkerboard.gfx_pieces = [[None for x in range(height)] for x in range(width)]

        for x in range(width):
            for y in range(height):

                if (x + y) % 2 != 0:
                    if y in range(3):
                        Checkerboard.gfx_pieces[x][y] = pyglet.sprite.Sprite(Resources.WHITE_PIECE)
                    elif y in range(3, height):
                        if (x % 2) == 0:
                            Checkerboard.gfx_pieces[x][y] = pyglet.sprite.Sprite(Resources.BLACK_PIECE)
                        else:
                            Checkerboard.gfx_pieces[x][y] = pyglet.sprite.Sprite(Resources.EMPTY)
                    else:
                        Checkerboard.gfx_pieces[x][y] = pyglet.sprite.Sprite(Resources.EMPTY)
                else:
                    Checkerboard.gfx_pieces[x][y] = pyglet.sprite.Sprite(Resources.EMPTY)

                Checkerboard.gfx_pieces[x][y].position = (x * 64, y * 64)
                Checkerboard.gfx_pieces[x][y].batch = batch

    @staticmethod
    def _initialize_logic(width, height):
        """Inserisce le pedine nere nella parte superiore della scacchiera e le
        pedine bianche nella parte inferiore della scacchiera"""

        Checkerboard.pieces = [[None for x in range(height)] for x in range(width)]

        for x in range(width):
            for y in range(height):

                if (x + y) % 2 != 0:
                    if y in range(3):
                        Checkerboard.pieces[x][y] = PieceEnum.WHITE_PIECE
                    elif y in range(3, height):
                        if (x % 2) == 0:
                            Checkerboard.pieces[x][y] = PieceEnum.BLACK_PIECE
                        else:
                            Checkerboard.pieces[x][y] = PieceEnum.EMPTY
                    else:
                       Checkerboard.pieces[x][y] = PieceEnum.EMPTY
                else:
                    Checkerboard.pieces[x][y] = PieceEnum.EMPTY
