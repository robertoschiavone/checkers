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

from Damiera import *
from EnumPedine import *
from Risorse import *
from Impostazioni import *
from Stato import *
from EnumCaselle import *
from Turno import *

import pyglet

def calcola_mosse_consentite(enum_turno, pedina, mosse = None):
    """
    Args:
        - turn:
        
        - piece: a tuple containing the integer coordinates of the piece to be
            considered

        - moves: 

    Kwargs:
        none

    Returns:
        a list of tuples, each tuple contains the coordinates of every tile that
        can be reached by the selected piece
    
    """
    
    enum_turno = EnumTurno()


    if mosse is None:
        mosse = list()

        x = pedina[0]
        y = pedina[1]

        mosse.append((x,y))


        if enum_turno == enum_turno.leggi_nero():
            if Checkerboard.pieces[x][y] == PieceEnum.BLACK_PIECE:
                pass
            elif Checkerboard.pieces[x][y] == PieceEnum.PROMOTED_BLACK_PIECE:
                pass

        elif enum_turno == enum_turno.get_white():
            if Checkerboard.pieces[x][y] == PieceEnum.WHITE_PIECE:
                
                if x < Settings.width - 1 and y < Settings.height - 1:
                    
                    if Checkerboard.pieces[x+1][y+1] == PieceEnum.BLACK_PIECE \
                    or Checkerboard.pieces[x+1][y+1] == \
                    PieceEnum.PROMOTED_BLACK_PIECE:
                    
                        #  ___ ___ ___
                        # |   |   |   |
                        # |   |   | # |
                        # |___|___|___|
                        # |   |   |   |
                        # |   | b |   |
                        # |___|___|___|
                        # |   |   |   |
                        # | w |   |   |
                        # |___|___|___|
                        #
                        if x + 2 < Settings.width and y + 2 < Settings.height:
                            if Checkerboard.pieces[x+2][y+2] == PieceEnum.EMPTY:
                                mosse.append((x+2, y+2))
                    #  ___ ___ ___
                    # |   |   |   |
                    # |   |   |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   | # |   |
                    # |___|___|___|
                    # |   |   |   |
                    # | w |   |   |
                    # |___|___|___|
                    #
                    elif Checkerboard.pieces[x+1][y+1] == PieceEnum.EMPTY:
                         mosse.append((x+1, y+1))

                    #  ___ ___ ___
                    # |   |   |   |
                    # |   |   |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   | # |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   |   | w |
                    # |___|___|___|
                    #
                if x > 0 and y < Settings.height - 1:
                    if Checkerboard.pieces[x-1][y+1] == PieceEnum.EMPTY:
                        mosse.append((x-1,y+1))
                    
                    elif Checkerboard.pieces[x-1][y+1] == PieceEnum.BLACK_PIECE \
                    or Checkerboard.pieces[x-1][y+1] == \
                    PieceEnum.PROMOTED_BLACK_PIECE:
                    
                        #  ___ ___ ___
                        # |   |   |   |
                        # | # |   |   |
                        # |___|___|___|
                        # |   |   |   |
                        # |   | b |   |
                        # |___|___|___|
                        # |   |   |   |
                        # |   |   | w |
                        # |___|___|___|
                        #
                        if x - 2 >= 0 and y + 2 < Settings.height:
                            if Checkerboard.pieces[x-2][y+2] == PieceEnum.EMPTY:
                                mosse.append((x-2, y+2))

            elif pieces[x][y] == PieceEnum.PROMOTED_WHITE_PIECE:
                pass

        for coords in mosse:
            pass

    return mosse

def calculate_result(move):
    """
    Args:
        - turn:
        
        - piece: a tuple containing the integer coordinates of the piece to be
            considered

        - moves: 

    Kwargs:
        none

    Returns:
        a list of tuples, each tuple contains the coordinates of every tile that
        can be reached by the selected piece
    
    """

    result = 0

    for index, coords in enumerate(move):
        if abs(coords[0] - move[index + 1][0]) > 1:
            x = coords[0] - 1
            y = coords[1] - 1
            eaten_piece = pieces[x][y]

            if eaten_piece == PieceEnum.BLACK_PIECE or eaten_piece == PieceEnum.WHITE_PIECE:
                result += 1
            elif eaten_piece == PieceEnum.PROMOTED_BLACK_PIECE or eaten_piece == PieceEnum.PROMOTED_WHITE_PIECE:
                result += 2

def find_best_move(moves):
    """
    Args:
        - turn:
        
        - piece: a tuple containing the integer coordinates of the piece to be
            considered

        - moves: 

    Kwargs:
        none

    Returns:
        a list of tuples, each tuple contains the coordinates of every tile that
        can be reached by the selected piece
    
    """

    max = 0
    index = 0

    for i, move in enumerate(moves):
        n = calculate_result(move)
        if n >= max:
            max = n
            index = i

    return moves[index]

def main():

    piece_enum = PieceEnum()

    pieces_batch = pyglet.graphics.Batch()
    tiles_batch = pyglet.graphics.Batch()

    settings = Settings(8, 8)

    turn = Turn()

    status = Status(turn.get_white())

    window = pyglet.window.Window(settings.get_width() * 64, settings.get_height() * 64, "Checkers")
    
    hightlighted_tiles = None

    checkerboard = Checkerboard(settings)

    @window.event
    def on_draw():
        """   """
        window.clear()
        checkerboard.draw()
    
    @window.event
    def on_close():
        window.has_exit = True
        exit(0)
        

    @window.event
    def on_mouse_press(coord_x, coord_y, button, modifiers):
        """   """
        if status.get_turn() == turn.get_white():

            x = coord_x // 64
            y = coord_y // 64

            if (x+y)%2 != 0:
                if checkerboard.get_piece(x, y) == piece_enum.get_white_piece():
                    if status.get_selected() is not None:
                        checkerboard.background[Status.selected[0]][Status.selected[1]].image = Risorse.BLACK_TILE
                    
                    status.set_selected(x, y)
                    Checkerboard.background[x][y].image = Risorse.SELECTED_TILE

                elif Checkerboard.pieces[x][y] == PieceEnum.BLACK_PIECE and Status.selected is not None:
                    Checkerboard.background[Status.selected[0]][Status.selected[1]].image = Risorse.BLACK_TILE
                    Status.selected = None
                else:
                    if Status.selected is not None:
                        if (x, y) != Status.selected and (x,y) in calcola_mosse_consentite(Status.turn, Status.selected):
                            Checkerboard.pieces[x][y] = PieceEnum.WHITE_PIECE
                            Checkerboard.pieces[Status.selected[0]][Status.selected[1]] = PieceEnum.EMPTY

                            Checkerboard.gfx_pieces[x][y].image = Risorse.WHITE_PIECE
                            Checkerboard.gfx_pieces[Status.selected[0]][Status.selected[1]].image = Risorse.EMPTY
                            
                            Status.selected = None
    
    while True:

        pyglet.clock.tick(True)

        if hightlighted_tiles == None:
            if Status.selected is not None:
                hightlighted_tiles = calcola_mosse_consentite(Status.turn, Status.selected)

                for i, coords in enumerate(hightlighted_tiles):
                    if i == 0:
                        Checkerboard.background[coords[0]][coords[1]].image = Risorse.SELECTED_TILE
                    else:
                        Checkerboard.background[coords[0]][coords[1]].image = Risorse.HIGHTLIGHTED_TILE
    
        else:
            if Status.selected is not None:
                for coords in hightlighted_tiles:
                    if coords != selected:
                        Checkerboard.background[coords[0]][coords[1]].image = Risorse.BLACK_TILE

                hightlighted_tiles = calcola_mosse_consentite(Status.turn, Status.selected)

                for i, coords in enumerate(hightlighted_tiles):
                    if i == 0:
                        Checkerboard.background[coords[0]][coords[1]].image = Risorse.SELECTED_TILE
                    else:
                        Checkerboard.background[coords[0]][coords[1]].image = Risorse.HIGHTLIGHTED_TILE
            else:
                for coords in hightlighted_tiles:
                    Checkerboard.background[coords[0]][coords[1]].image = Risorse.BLACK_TILE
        
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        turn = switch_turn(turn)
        window.flip()

if __name__ == "__main__":
    main()
