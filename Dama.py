from Damiera import *
from EnumPedine import *
from Risorse import *
from EnumTurno import *

import pyglet
import time


def main():

    lato = 8

    window = pyglet.window.Window(lato*64, lato*64, 'Dama')

    caselle_evidenziate = None

    damiera = Damiera(lato, euristica="MM", turno_iniziale=EnumTurno.NERO)

    @window.event
    def on_draw():
        window.clear()
        damiera.draw()

    @window.event
    def on_close():
        pass

    @window.event
    def on_mouse_press(coord_x, coord_y, button, modifiers):

        x = coord_x // 64
        y = coord_y // 64

        if damiera.get_turno() == EnumTurno.BIANCO:

            if (x + y) % 2 != 0:
                if damiera.damiera[x][y]  == EnumPedine.PEDINA_BIANCA:
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

        else:
            if (x + y) % 2 != 0:
                if damiera.leggi_pedina(x, y) == EnumPedine.PEDINA_NERA:

                    damiera.set_selezionato((x, y))

                elif damiera.leggi_pedina(x, y) == EnumPedine.PEDINA_BIANCA \
                    and damiera.get_selezionato() is not None:
                    damiera.set_selezionato(None)
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

if __name__ == '__main__':
    main()
