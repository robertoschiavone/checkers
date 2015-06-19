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

def minimax(nodo, profondita, massimizzare, damiera):
    if profondita == 0: # oppure l'insieme di mosse porta in vantaggio l'AI,
       # cioè l'azione si conclude con una pedina mangiata da parte dell'AI,
       # a cui il giocatore non può rispondere con la mossa immediatamente successiva
        return calcola_risultato(calcola_mossa_migliore(damiera, nodo))
    
    if massimizzare == True:
        risultato = Float("-inf")
        for mossa in nodo:
            valore = minimax(mossa, profondita - 1, False)
    
            risultato = max(risultato, valore)
    
        return risultato
    else:
        risultato = Float("+inf")
        for mossa in nodo:
            valore = minimax(mossa, profondita - 1, True)

            risultato = max(risultato, valore)
        
            return risultato



def calcola_mosse_consentite(damiera, impostazioni, turno, pedina, mosse = None):

    enum_turno = EnumTurno()
    enum_pedine = EnumPedine()

    if mosse is None:
        mosse = list()

        x = pedina[0]
        y = pedina[1]

        mosse.append((x,y))

    if turno == enum_turno.leggi_nero():
        if damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_nera() or \
            damiera.leggi_pedina(x, y) == enum_pedine.leggi_dama_nera():
                
            if x < impostazioni.leggi_larghezza() - 1 and y > 0:
                    
                if damiera.leggi_pedina(x-1, y-1) == enum_pedine.leggi_pedina_bianca() \
                or damiera.leggi_pedina(x-1, y-1) == \
                enum_pedine.leggi_dama_bianca():

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
                        if damiera.leggi_pedina(x-2, y-2) == enum_pedine.leggi_vuoto():
                            mosse.append((x-2, y-2))
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
                elif damiera.leggi_pedina(x-1, y-1) == enum_pedine.leggi_vuoto():
                        mosse.append((x-1, y-1))

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
            if x > 0 and y < impostazioni.leggi_altezza() - 1:
                if damiera.leggi_pedina(x-1, y+1) == enum_pedine.leggi_vuoto():
                    mosse.append((x-1,y+1))
                    
                elif damiera.leggi_pedina(x-1, y+1) == enum_pedine.leggi_pedina_nera() \
                or damiera.leggi_pedina(x-1, y+1) == \
                enum_pedine.leggi_dama_nera():
                    
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
                    if x - 2 >= 0 and y + 2 < impostazioni.leggi_altezza():
                        if damiera.leggi_pedina(x-2, y+2) == enum_pedine.leggi_vuoto():
                            mosse.append((x-2, y+2))

        if damiera.leggi_pedina(x, y) == enum_pedine.leggi_dama_bianca():
            pass

    elif turno == enum_turno.leggi_bianco():
        if damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_bianca() or \
            damiera.leggi_pedina(x, y) == enum_pedine.leggi_dama_bianca():
                
            if x < impostazioni.leggi_larghezza() - 1 and y < impostazioni.leggi_altezza() - 1:
                    
                if damiera.leggi_pedina(x+1, y+1) == enum_pedine.leggi_pedina_nera() \
                or damiera.leggi_pedina(x+1, y+1) == \
                enum_pedine.leggi_dama_nera():

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
                    if x + 2 < enum_pedine.leggi_pedina_nera() and y + 2 < impostazioni.leggi_altezza():
                        if damiera.leggi_pedina(x+2, y+2) == enum_pedine.leggi_vuoto():
                            mosse.append((x+2, y+2))
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
                elif damiera.leggi_pedina(x+1, y+1) == enum_pedine.leggi_vuoto():
                        mosse.append((x+1, y+1))

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
                if damiera.leggi_pedina(x-1, y+1) == enum_pedine.leggi_vuoto():
                    mosse.append((x-1,y+1))
                    
                elif damiera.leggi_pedina(x-1, y+1) == enum_pedine.leggi_pedina_nera() \
                or damiera.leggi_pedina(x-1, y+1) == \
                enum_pedine.leggi_dama_nera():
                    
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
                    if x - 2 >= 0 and y + 2 < impostazioni.leggi_altezza():
                        if damiera.leggi_pedina(x-2, y+2) == enum_pedine.leggi_vuoto():
                            mosse.append((x-2, y+2))

        if damiera.leggi_pedina(x, y) == enum_pedine.leggi_dama_bianca():
            pass

    for coord in mosse:
        pass

    return mosse

def calcola_risultato(damiera, mossa):

    risultato = 0

    enum_pedine = EnumPedine()

    for indice, coord in enumerate(mossa):
        if abs(coord[0] - mossa[indice + 1][0]) > 1:
            x = coord[0] - 1
            y = coord[1] - 1
            pedina_catturata = damiera.leggi_pedina(x, y)

            if pedina_catturata == enum_pedine.leggi_pedina_nera() or pedina_catturata == enum_pedine.leggi_pedina_bianca():
                risultato += 1
            elif pedina_catturata == enum_pedine.leggi_dama_nera() or pedina_catturata == enum_pedine.leggi_dama_bianca():
                risultato += 2

    return risultato


def calcola_insieme_mosse(damiera, impostazioni, turno):

    enum_turno = EnumTurno()

    enum_pedine = EnumPedine()

    lista_liste_mosse = list()

    if turno == enum_turno.leggi_bianco():
        for x in range(impostazioni.leggi_larghezza()):
            for y in range(impostazioni.leggi_altezza()):
                if damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_bianca() or \
                    damiera.leggi_pedina(x, y) == enum_pedine.leggi_dama_bianca():

                    lista_liste_mosse.append(calcola_mosse_consentite(damiera, impostazioni, turno, (x, y)))

    else:
        for x in range(impostazioni.leggi_larghezza()):
            for y in range(impostazioni.leggi_altezza()):
                if damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_nera() or \
                    damiera.leggi_pedina(x, y) == enum_pedine.leggi_dama_nera():

                    lista_liste_mosse.append(calcola_mosse_consentite(damiera, impostazioni, turno, (x, y)))

    max = 0


    for lista in lista_liste_mosse:
        if calcola_risultato(damiera, calcola_mossa_migliore(damiera, lista)) >= max:
            max = calcola_risultato(damiera, calcola_mossa_migliore(damiera, lista))


def calcola_mossa_migliore(damiera, mosse):

    max = 0
    indice = 0

    for i, mossa in enumerate(mosse):
        n = calcola_risultato(damiera, mossa)
        if n >= max:
            max = n
            indice = i

    return mosse[indice]

def main():

    enum_pedine = EnumPedine()

    impostazioni = Impostazioni(8, 8)

    enum_turno = EnumTurno()

    stato = Stato(enum_turno.leggi_bianco())

    window = pyglet.window.Window(impostazioni.leggi_larghezza() * 64, \
        impostazioni.leggi_altezza() * 64, "Checkers")
    
    caselle_evidenziate = None

    damiera = Damiera(impostazioni)

    @window.event
    def on_draw():
        """   """
        window.clear()
        damiera.draw()
    
    @window.event
    def on_close():
        window.has_exit = True
        exit(0)
        
    risorse = Risorse()

    @window.event
    def on_mouse_press(coord_x, coord_y, button, modifiers):
        """   """

        x = coord_x // 64
        y = coord_y // 64

        if stato.leggi_turno() == enum_turno.leggi_bianco():

            if (x+y)%2 != 0:
                if damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_bianca():
                    if stato.leggi_selezionato() is not None:
                        damiera.cambia_casella(stato.leggi_selezionato(), risorse.leggi_casella_nera())

                    stato.scrivi_selezionato((x, y))
                    damiera.cambia_casella((x, y), risorse.leggi_casella_selezionata())

                elif damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_nera() and stato.leggi_selezionato() is not None:
                    damiera.cambia_casella(stato.leggi_selezionato(), risorse.leggi_casella_nera())
                    stato.scrivi_selezionato(None)
                else:
                    if stato.leggi_selezionato() is not None:
                        if (x, y) != stato.leggi_selezionato()and (x,y) in \
                            calcola_mosse_consentite(damiera, impostazioni,\
                            stato.leggi_turno(), stato.leggi_selezionato()):
                            
                            damiera.cambia_pedina((x, y), \
                                stato.leggi_selezionato(), \
                                enum_pedine.leggi_pedina_bianca())
                            stato.scrivi_selezionato(None)
                            stato.cambia_turno()
                            
                            
#                            minimax(calcola_mosse_consentite(damiera, impostazioni, stato.leggi_turno(), pedina),
 #                                   0, True, damiera)

 #                           stato.cambia_turno()
        else:
            if (x+y)%2 != 0:
                if damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_nera():
                    if stato.leggi_selezionato() is not None:
                        damiera.cambia_casella(stato.leggi_selezionato(), risorse.leggi_casella_nera())

                    stato.scrivi_selezionato((x, y))
                    damiera.cambia_casella((x, y), risorse.leggi_casella_selezionata())

                elif damiera.leggi_pedina(x, y) == enum_pedine.leggi_pedina_bianca() and stato.leggi_selezionato() is not None:
                    damiera.cambia_casella(stato.leggi_selezionato(), risorse.leggi_casella_nera())
                    stato.scrivi_selezionato(None)
                else:
                    if stato.leggi_selezionato() is not None:
                        if (x, y) != stato.leggi_selezionato()and (x,y) in \
                            calcola_mosse_consentite(damiera, impostazioni,\
                            stato.leggi_turno(), stato.leggi_selezionato()):
                            
                            damiera.cambia_pedina((x, y), \
                                stato.leggi_selezionato(), \
                                enum_pedine.leggi_pedina_nera())
                            stato.scrivi_selezionato(None)
                            stato.cambia_turno()
                            #minimax
#                            stato.cambia_turno()

   
    while True:

        pyglet.clock.tick(True)

        if caselle_evidenziate == None:
            if stato.leggi_selezionato() is not None:
                caselle_evidenziate = calcola_mosse_consentite(damiera, impostazioni, stato.leggi_turno(), stato.leggi_selezionato())

                for i, coord in enumerate(caselle_evidenziate):
                    if i == 0:
                        damiera.cambia_casella(coord, risorse.leggi_casella_selezionata())
                    else:
                        damiera.cambia_casella(coord, risorse.leggi_casella_evidenziata())
    
        else:
            if stato.leggi_selezionato() is not None:
                for coord in caselle_evidenziate:
                    if coord != stato.leggi_selezionato():
                        damiera.cambia_casella(coord, risorse.leggi_casella_nera())

                caselle_evidenziate = calcola_mosse_consentite(damiera, impostazioni, stato.leggi_turno(), stato.leggi_selezionato())

                for i, coord in enumerate(caselle_evidenziate):
                    if i == 0:
                        damiera.cambia_casella(coord, risorse.leggi_casella_selezionata())
                    else:
                        damiera.cambia_casella(coord, risorse.leggi_casella_evidenziata())
            else:
                for coord in caselle_evidenziate:
                    damiera.cambia_casella(coord, risorse.leggi_casella_nera())
        

        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()

if __name__ == "__main__":
    main()
