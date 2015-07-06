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
from EnumTurno import *

import getopt
import pyglet
import sys


def main(args):

    parametri, valori = getopt.getopt(args, "h", ["profondita=", "lato=", 
                                                  "algoritmo=", "colore="])

    lato = 8

    turno_iniziale = EnumTurno.BIANCO

    euristica = "AB"

    profondita = 4

    for par, val in parametri:

        if par == "--lato":
            lato = int(val)
        
        if par == "--colore":
            if val == "nero":
                turno_iniziale = EnumTurno.NERO

        if par == "--algoritmo":
            if val == "MM":
                euristica = "MM"

        if par == "--profondita":
            profondita = int(val)

        if par == "-h":
            print("Parametri:\n--profondita=n\n--lato=n\n--euristica=MM/AB\n--colore=bianco/nero")
            exit(0)

    window = pyglet.window.Window(lato*64, lato*64, 'Dama')

    caselle_evidenziate = None

    damiera = Damiera(lato, euristica, turno_iniziale=turno_iniziale, profondita=profondita)

    @window.event
    def on_draw():
        window.clear()
        damiera.draw()

    @window.event
    def on_close():
        exit(0)

    @window.event
    def on_mouse_press(coord_x, coord_y, button, modifiers):

        x = coord_x // 64
        y = coord_y // 64

        if damiera.get_turno() == damiera.get_turno_iniziale():

            if (x + y) % 2 != 0:
                if damiera.damiera[x][y]  == EnumPedine(damiera.get_turno()) or\
                 damiera.damiera[x][y]  == EnumPedine(damiera.get_turno()+2):
                    damiera.set_selezionato((x, y))

                else:
                    if damiera.get_selezionato() is not None:

                        if (x, y) != damiera.get_selezionato():
                            mosse_consentite = damiera.calcola_mosse_pedina(damiera.get_selezionato())
                            
                            for mossa in mosse_consentite:
                                if mossa.fine == (x, y):
                                    damiera.set_selezionato(None)
                                    damiera.muovi(mossa)
                                    damiera.cambia_turno()
                                    window.dispatch_event("on_draw")
                                   

    while True:
        pyglet.clock.tick(True)
        
        window.dispatch_events()

        window.dispatch_event('on_draw')
        window.flip()
        
        if damiera.get_turno() != damiera.get_turno_iniziale():
            mossa = damiera.calcola_mossa_migliore()
            damiera.muovi(mossa)

            window.dispatch_event('on_draw')

            damiera.cambia_turno()
        
        

        if damiera.calcola_pedine_nere() == 0:
            print("Bianco vince")
            exit(0)

        if damiera.calcola_pedine_bianche() == 0:
            print("Nero vince")
            exit(0)

        if damiera.calcola_pedine() < 4:
            if contatore_stallo is None:
                contatore_stallo = 30
            elif contatore_stallo > 1:
                contatore_stallo -= 1
            else:
                print('Fine partita per stallo')
                exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
