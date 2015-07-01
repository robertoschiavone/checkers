from Damiera import *
from EnumPedine import *
from Risorse import *
from EnumTurno import *

import pyglet

def minimax(nodo, profondita, massimizzare, damiera):
    if profondita == 0:
        return calcola_risultato(calcola_mossa_migliore(damiera, nodo))

    if massimizzare == True:
        risultato = Float('-inf')
        for mossa in nodo:
            valore = minimax(mossa, profondita - 1, False)

            risultato = max(risultato, valore)

        return risultato
    else:
        risultato = Float('+inf')
        for mossa in nodo:
            valore = minimax(mossa, profondita - 1, True)

            risultato = max(risultato, valore)

            return risultato

def calcola_mosse_consentite(damiera, turno, pedina):

    x = pedina[0]
    y = pedina[1]

    mosse_consentite = list()
    mosse_consentite.append(pedina)

    if turno == EnumTurno.leggi_nero():
        if damiera.leggi_pedina(x, y) \
            == EnumPedine.leggi_pedina_nera() \
            or damiera.leggi_pedina(x, y) \
            == EnumPedine.leggi_dama_nera():

            if x < impostazioni.leggi_larghezza() - 1 and y > 0:

                if damiera.leggi_pedina(x - 1, y - 1) \
                    == EnumPedine.leggi_pedina_bianca() \
                    or damiera.leggi_pedina(x - 1, y - 1) \
                    == EnumPedine.leggi_dama_bianca():

                    #  ___ ___ ___
                    # |   |   |   |
                    # |   |   | N |
                    # |___|___|___|
                    # |   |   |   |
                    # |   | B |   |
                    # |___|___|___|
                    # |   |   |   |
                    # | # |   |   |
                    # |___|___|___|
                    #

                    if x - 2 >= 0 and y - 2 >= 0:
                        if damiera.leggi_pedina(x - 2, y - 2) \
                            == EnumPedine.leggi_vuoto():
                            mosse_consentite.append((x - 2, y - 2))
                #  ___ ___ ___
                # |   |   |   |
                # |   |   | N |
                # |___|___|___|
                # |   |   |   |
                # |   | # |   |
                # |___|___|___|
                # |   |   |   |
                # |   |   |   |
                # |___|___|___|
                #
                elif damiera.leggi_pedina(x - 1, y - 1) \
                    == EnumPedine.leggi_vuoto():

                    mosse_consentite.append((x - 1, y - 1))

                #  ___ ___ ___
                # |   |   |   |
                # | N |   |   |
                # |___|___|___|
                # |   |   |   |
                # |   | # |   |
                # |___|___|___|
                # |   |   |   |
                # |   |   |   |
                # |___|___|___|
                #

            if x < impostazioni.leggi_larghezza() - 1 and y > 1:
                if damiera.leggi_pedina(x + 1, y - 1) \
                    == EnumPedine.leggi_vuoto():
                    mosse_consentite.append((x + 1, y - 1))

                elif damiera.leggi_pedina(x + 1, y - 1) \
                    == EnumPedine.leggi_pedina_bianca() \
                    or damiera.leggi_pedina(x + 1, y - 1) \
                    == EnumPedine.leggi_dama_bianca():

                    #  ___ ___ ___
                    # |   |   |   |
                    # | N |   |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   | B |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   |   | # |
                    # |___|___|___|
                    #

                    if x + 2 < impostazioni.leggi_larghezza() and y - 2 >= 0:
                        if damiera.leggi_pedina(x + 2, y - 2) \
                            == EnumPedine.leggi_vuoto():
                            mosse_consentite.append((x + 2, y - 2))

        if damiera.leggi_pedina(x, y) \
            == EnumPedine.leggi_dama_bianca():
            pass

    elif turno == EnumTurno.leggi_bianco():

        if damiera.leggi_pedina(x, y) \
            == EnumPedine.leggi_pedina_bianca() \
            or damiera.leggi_pedina(x, y) \
            == EnumPedine.leggi_dama_bianca():
            if x < impostazioni.leggi_larghezza() - 1 and y \
                < impostazioni.leggi_altezza() - 1:

                if damiera.leggi_pedina(x + 1, y + 1) \
                    == EnumPedine.leggi_pedina_nera() \
                    or damiera.leggi_pedina(x + 1, y + 1) \
                    == EnumPedine.leggi_dama_nera():

                    #  ___ ___ ___
                    # |   |   |   |
                    # |   |   | # |
                    # |___|___|___|
                    # |   |   |   |
                    # |   | N |   |
                    # |___|___|___|
                    # |   |   |   |
                    # | B |   |   |
                    # |___|___|___|
                    #

                    if x + 2 <= impostazioni.leggi_larghezza() and y \
                        + 2 < impostazioni.leggi_altezza():
                        if damiera.leggi_pedina(x + 2, y + 2) \
                            == EnumPedine.leggi_vuoto():
                            mosse_consentite.append(x + 2, y + 2)
                elif damiera.leggi_pedina(x + 1, y + 1) \
                    == EnumPedine.leggi_vuoto():

                #  ___ ___ ___
                # |   |   |   |
                # |   |   |   |
                # |___|___|___|
                # |   |   |   |
                # |   | # |   |
                # |___|___|___|
                # |   |   |   |
                # | B |   |   |
                # |___|___|___|
                #

                    mosse_consentite.append((x + 1, y + 1))

                #  ___ ___ ___
                # |   |   |   |
                # |   |   |   |
                # |___|___|___|
                # |   |   |   |
                # |   | # |   |
                # |___|___|___|
                # |   |   |   |
                # |   |   | B |
                # |___|___|___|
                #

            if x > 0 and y < impostazioni.leggi_altezza() - 1:
                if damiera.leggi_pedina(x - 1, y + 1) \
                    == EnumPedine.leggi_vuoto():
                    mosse_consentite.append((x - 1, y + 1))
                elif damiera.leggi_pedina(x - 1, y + 1) \
                    == EnumPedine.leggi_pedina_nera() \
                    or damiera.leggi_pedina(x - 1, y + 1) \
                    == EnumPedine.leggi_dama_nera():

                    #  ___ ___ ___
                    # |   |   |   |
                    # | # |   |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   | N |   |
                    # |___|___|___|
                    # |   |   |   |
                    # |   |   | B |
                    # |___|___|___|
                    #

                    if x - 2 >= 0 and y + 2 \
                        < impostazioni.leggi_altezza():
                        if damiera.leggi_pedina(x - 2, y + 2) \
                            == EnumPedine.leggi_vuoto():
                            mosse_consentite.append((x - 2, y + 2))

        if damiera.leggi_pedina(x, y) \
            == EnumPedine.leggi_dama_bianca():
            pass

    for coord in mosse_consentite:
        pass

    return mosse_consentite

def calcola_risultato(damiera, mossa):

    risultato = 0

    EnumPedine = EnumPedine()

    for (indice, coord) in enumerate(mossa):
        if abs(coord[0] - mossa[indice + 1][0]) > 1:
            x = coord[0] - 1
            y = coord[1] - 1
            pedina_catturata = damiera.leggi_pedina(x, y)

            if pedina_catturata == EnumPedine.leggi_pedina_nera() \
                or pedina_catturata \
                == EnumPedine.leggi_pedina_bianca():
                risultato += 1
            elif pedina_catturata == EnumPedine.leggi_dama_nera() \
                or pedina_catturata == EnumPedine.leggi_dama_bianca():
                risultato += 2

    return risultato

def calcola_insieme_mosse(damiera, turno):

    lista_liste_mosse = list()

    if turno == EnumTurno.leggi_bianco():
        for x in range(impostazioni.leggi_larghezza()):
            for y in range(impostazioni.leggi_altezza()):
                if damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_pedina_bianca() \
                    or damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_dama_bianca():

                    lista_liste_mosse.append(calcola_mosse_consentite(damiera,
                            impostazioni, turno, (x, y)))
    else:

        for x in range(impostazioni.leggi_larghezza()):
            for y in range(impostazioni.leggi_altezza()):
                if damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_pedina_nera() \
                    or damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_dama_nera():

                    lista_liste_mosse.append(calcola_mosse_consentite(damiera,
                            impostazioni, turno, (x, y)))

    max = 0

    for lista in lista_liste_mosse:
        if calcola_risultato(damiera, calcola_mossa_migliore(damiera,
                             lista)) >= max:
            max = calcola_risultato(damiera,
                                    calcola_mossa_migliore(damiera,
                                    lista))

def calcola_mossa_migliore(damiera, mosse):

    max = 0
    indice = 0

    for (i, mossa) in enumerate(mosse):
        n = calcola_risultato(damiera, mossa)
        if n >= max:
            max = n
            indice = i

    return mosse[indice]

def main():

    lato = 6

    window = pyglet.window.Window(lato*64, lato*64, 'Dama')

    caselle_evidenziate = None

    damiera = Damiera(lato)

    @window.event
    def on_draw():
        """   """

        window.clear()
        damiera.draw()

    @window.event
    def on_close():
        window.has_exit = True
        exit(0)

    @window.event
    def on_mouse_press(coord_x, coord_y, button, modifiers):
        """   """

        x = coord_x // 64
        y = coord_y // 64

        if damiera.get_turno() == damiera.get_turno_iniziale():

            if (x + y) % 2 != 0:
                if damiera.damiera[x][y]  == damiera.get_turno_iniziale():
                    stato.scrivi_selezionato((x, y))

                elif damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_pedina_nera() \
                    and stato.leggi_selezionato() is not None:

                    stato.scrivi_selezionato(None)
                else:
                    if stato.leggi_selezionato() is not None:
                        if (x, y) != stato.leggi_selezionato() and (x,
                                y) in calcola_mosse_consentite(damiera,
                                impostazioni, stato.leggi_turno(),
                                stato.leggi_selezionato()):

                            stato.scrivi_selezionato(None)

                    stato.cambia_turno()
        else:
            if (x + y) % 2 != 0:
                if damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_pedina_nera():

                    stato.scrivi_selezionato((x, y))

                elif damiera.leggi_pedina(x, y) \
                    == EnumPedine.leggi_pedina_bianca() \
                    and stato.leggi_selezionato() is not None:
                    stato.scrivi_selezionato(None)
                else:
                    if stato.leggi_selezionato() is not None:
                        if (x, y) != stato.leggi_selezionato() and (x,
                                y) in calcola_mosse_consentite(damiera,
                                impostazioni, stato.leggi_turno(),
                                stato.leggi_selezionato()):

                            stato.scrivi_selezionato(None)
                            
                        stato.cambia_turno()

    while True:

        pyglet.clock.tick(True)

        if caselle_evidenziate == None:
            if damiera.get_selezionato() is not None:
                caselle_evidenziate = calcola_mosse_consentite(damiera, 
                    stato.leggi_turno(), stato.leggi_selezionato())


        else:
            if stato.leggi_selezionato() is not None:
               
                caselle_evidenziate = calcola_mosse_consentite(damiera,
                        impostazioni, stato.leggi_turno(),
                        stato.leggi_selezionato())

        if damiera.get_turno() == EnumTurno.NERO:
            print(calcola_insieme_mosse(damiera, impostazioni, stato.leggi_turno()))
            minimax(calcola_insieme_mosse(damiera, impostazioni, stato.leggi_turno()), 6, 
                    True, damiera)
            damiera.set_turno(1 - damiera.get_turno())

        if damiera.calcola_pedine() < 4:
            if contatore_stallo is None:
                contatore_stallo = 30
            elif contatore_stallo > 1:
                contatore_stallo -= 1
            else:
                print('Fine partita per STALLO')

        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()


if __name__ == '__main__':
    main()

