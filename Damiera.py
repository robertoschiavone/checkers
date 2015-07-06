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
from EnumPedine import *
from EnumTurno import *
from Mossa import *
from Risorse import *

import copy
import pyglet

class Damiera:

    def __init__(self, lato, euristica="AB", pedine=[], turno_iniziale = EnumTurno.BIANCO, selezionato=None, profondita=4):
        """
        Inizializza la damiera,, creando le opportune strutture i dati per 
        gestire le pedine, le caselle e la logica di gioco

        Parametri:
            - lato: oggetto contenente le informazioni di altezza e
            larghezza, necessarie per la corretta inizializzazione della damiera
        """

        self.profondita = profondita

        self.euristica = euristica
        
        self.turno = EnumTurno.BIANCO
        self.turno_iniziale = turno_iniziale

        self.lato = lato

        self.selezionato = selezionato

        self.mossa_ai = None

        if not pedine:
            self.damiera = [[None for x in range(lato)] for x in range(lato)]

            # popola la matrice che tiene traccia delle posizioni delle pedine
            for x in range(lato):
                for y in range(lato):

                    if (x + y) % 2 != 0:
                        # inserisce le pedine bianche nelle prime 3 file
                        if y in range(self.lato//2-1):
                            self.damiera[x][y] = EnumPedine.PEDINA_BIANCA

                        # inserisce le pedine nere nelle ultime 3 file
                        elif y in range(self.lato//2+1, self.lato):
                            self.damiera[x][y] = EnumPedine.PEDINA_NERA
                        else:
                           self.damiera[x][y] = EnumPedine.VUOTO
                    else:
                        self.damiera[x][y] = EnumPedine.VUOTO
        
        else:
            self.damiera = pedine



    def leggi_pedina(self, x, y):
        return self.damiera[x][y]



    def get_selezionato(self):
        return self.selezionato



    def set_selezionato(self, coordinate):
        self.selezionato = coordinate



    def get_turno(self):
        return self.turno



    def get_turno_iniziale(self):
        return self.turno_iniziale



    def draw(self):
        risorse = Risorse()

        batch_caselle = pyglet.graphics.Batch()
        batch_pedine = pyglet.graphics.Batch()
        
        sfondo = [[None for x in range(self.lato)] for x in range(self.lato)]
        pedine = [[None for x in range(self.lato)] for x in range(self.lato)]

        for x in range(self.lato):
            for y in range(self.lato):
                if (x + y) % 2 == 0:
                    sfondo[x][y] = pyglet.sprite.Sprite(risorse.leggi_casella_bianca())
                else:
                    sfondo[x][y] = pyglet.sprite.Sprite(risorse.leggi_casella_nera())

                sfondo[x][y].batch = batch_caselle
                sfondo[x][y].position = (x * 64, y * 64)

        if self.selezionato is not None:
            sfondo[self.selezionato[0]][self.selezionato[1]].image = risorse.leggi_casella_selezionata()

            mosse_consentite = self.calcola_mosse_pedina(self.selezionato)

            for mossa in mosse_consentite:
                sfondo[mossa.fine[0]][mossa.fine[1]].image = risorse.leggi_casella_evidenziata()


        for x in range(self.lato):
            for y in range(self.lato):

                if self.damiera[x][y] == EnumPedine.PEDINA_BIANCA:
                    pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_pedina_bianca())

                elif self.damiera[x][y] == EnumPedine.PEDINA_NERA:
                    pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_pedina_nera())

                elif self.damiera[x][y] == EnumPedine.DAMA_BIANCA:
                    pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_dama_bianca())

                elif self.damiera[x][y] == EnumPedine.DAMA_NERA:
                    pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_dama_nera())
            
                else:
                    pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_vuoto())

                pedine[x][y].position = (x * 64, y * 64)
                pedine[x][y].batch = batch_pedine

        batch_caselle.draw()
        batch_pedine.draw()



    def calcola_mosse_pedina(self, pedina):

        x = pedina[0]
        y = pedina[1]

        mosse_consentite = list()

        if self.turno == EnumTurno.NERO:
            if self.leggi_pedina(x, y)  == EnumPedine.PEDINA_NERA \
                or self.leggi_pedina(x, y) == EnumPedine.DAMA_NERA:

                if x < self.lato and y > 0:

                    if self.leggi_pedina(x-1, y-1) == EnumPedine.PEDINA_BIANCA \
                        or self.leggi_pedina(x-1, y-1) == EnumPedine.DAMA_BIANCA:

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

                        if x-2 >= 0 and y-2 >= 0:
                            if self.leggi_pedina(x-2, y-2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x-2, y-2), (x-1, y-1))
                                mosse_consentite.append(mossa)
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
                    elif x > 0:
                        if self.leggi_pedina(x-1, y-1) == EnumPedine.VUOTO:
                            if(x-1, y-1) == (-1,4):
                                print((x-1, y-1))
                                print("Qui")
                            mossa = Mossa((x, y), (x-1, y-1))
                            mosse_consentite.append(mossa)

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

                if x < self.lato-1 and y > 1:
                    if self.leggi_pedina(x+1, y-1) == EnumPedine.VUOTO:
                        mossa = Mossa((x, y), (x+1, y-1))
                        mosse_consentite.append(mossa)

                    elif self.leggi_pedina(x+1, y-1) == EnumPedine.PEDINA_BIANCA \
                        or self.leggi_pedina(x+1, y-1) == EnumPedine.DAMA_BIANCA:

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

                        if x+2 < self.lato and y-2 >= 0:
                            if self.leggi_pedina(x+2, y-2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x+2, y-2), (x+1, y-1))
                                mosse_consentite.append(mossa)

            if self.leggi_pedina(x, y) \
                == EnumPedine.DAMA_NERA:

                if x < self.lato-1 and y  < self.lato-1:

                    if self.leggi_pedina(x+1, y+1) == EnumPedine.PEDINA_BIANCA \
                        or self.leggi_pedina(x+1, y+1) == EnumPedine.DAMA_BIANCA:

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

                        if x+2 < self.lato and y+2 < self.lato:
                            if self.leggi_pedina(x+2, y+2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x+2, y+2), (x+1, y+1))
                                mosse_consentite.append(mossa)

                    elif self.leggi_pedina(x+1, y+1) == EnumPedine.VUOTO:

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

                        mossa = Mossa((x, y), (x+1, y+1))
                        mosse_consentite.append(mossa)

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

                if x > 0 and y < self.lato-1:
                    if self.leggi_pedina(x-1, y+1) == EnumPedine.VUOTO:
                        mossa = Mossa((x, y), (x-1, y+1))
                        mosse_consentite.append(mossa)

                    elif self.leggi_pedina(x-1, y+1) == EnumPedine.PEDINA_BIANCA \
                        or self.leggi_pedina(x-1, y+1) == EnumPedine.DAMA_BIANCA:

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

                        if x-2 >= 0 and y+2  < self.lato:
                            if self.leggi_pedina(x-2, y+2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x-2, y+2), (x-1, y+1))
                                mosse_consentite.append(mossa)


        elif self.turno == EnumTurno.BIANCO:

            if self.leggi_pedina(x, y)  == EnumPedine.PEDINA_BIANCA \
                or self.leggi_pedina(x, y)  == EnumPedine.DAMA_BIANCA:
                if x < self.lato-1 and y  < self.lato-1:

                    if self.leggi_pedina(x+1, y+1) == EnumPedine.PEDINA_NERA \
                        or self.leggi_pedina(x+1, y+1) == EnumPedine.DAMA_NERA:

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

                        if x+2 <= self.lato and y+2 < self.lato:
                            if self.leggi_pedina(x+2, y+2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x+2, y+2), (x+1, y+1))
                                mosse_consentite.append(mossa)

                    elif self.leggi_pedina(x+1, y+1) == EnumPedine.VUOTO:

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

                        mossa = Mossa((x, y), (x+1, y+1))
                        mosse_consentite.append(mossa)

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

                if x > 0 and y < self.lato-1:
                    if self.leggi_pedina(x-1, y+1) == EnumPedine.VUOTO:
                        mossa = Mossa((x, y), (x-1, y+1))
                        mosse_consentite.append(mossa)

                    elif self.leggi_pedina(x-1, y+1) == EnumPedine.PEDINA_NERA \
                        or self.leggi_pedina(x-1, y+1) == EnumPedine.DAMA_NERA:

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

                        if x-2 >= 0 and y+2  < self.lato:
                            if self.leggi_pedina(x-2, y+2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x-2, y+2), (x-1, y+1))
                                mosse_consentite.append(mossa)

            if self.leggi_pedina(x, y) == EnumPedine.DAMA_BIANCA:

                if x < self.lato and y > 0:

                    if self.leggi_pedina(x-1, y-1) == EnumPedine.PEDINA_NERA \
                        or self.leggi_pedina(x-1, y-1) == EnumPedine.DAMA_NERA:

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

                        if x-2 >= 0 and y-2 >= 0:
                            if self.leggi_pedina(x-2, y-2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x-2, y-2), (x-1, y-1))
                                mosse_consentite.append(mossa)
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
                    elif self.leggi_pedina(x-1, y-1) == EnumPedine.VUOTO:
                        mossa = Mossa((x, y), (x-1, y-1))
                        mosse_consentite.append(mossa)

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

                if x < self.lato-1 and y > 1:
                    if self.leggi_pedina(x+1, y-1) == EnumPedine.VUOTO:
                        mossa = Mossa((x, y), (x+1, y-1))
                        mosse_consentite.append(mossa)

                    elif self.leggi_pedina(x+1, y-1) == EnumPedine.PEDINA_BIANCA \
                        or self.leggi_pedina(x+1, y-1) == EnumPedine.DAMA_BIANCA:

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

                        if x+2 < self.lato and y-2 >= 0:
                            if self.leggi_pedina(x+2, y-2) == EnumPedine.VUOTO:
                                mossa = Mossa((x, y), (x+2, y-2), (x+1, y-1))
                                mosse_consentite.append(mossa)

        return mosse_consentite



    def calcola_punteggio(self, turno):
        
        risultato = 0

        for x in range(self.lato):
            for y in range(self.lato):
                if self.turno == EnumTurno.BIANCO:
                    if self.damiera[x][y] == EnumPedine.PEDINA_BIANCA:
                        risultato += 1
                        if (y == 0 or y == self.lato-1) and (x == 0 or \
                            x == self.lato-1):
                            risultato += 0.5

                        elif (x <= self.lato//2 + 1 and \
                            x >= self.lato//2 + 1) and \
                            (y <= self.lato//2 + 1 and \
                            y >= self.lato//2 + 1):
                            risultato += 0.25

                    elif self.damiera[x][y] == EnumPedine.DAMA_BIANCA:
                        risultato += 3
                        
                        if (y == 0 or y == self.lato-1) and (x == 0 or \
                            x == self.lato-1):
                            risultato += 0.5

                        elif (x <= self.lato//2 + 1 and \
                            x >= self.lato//2 + 1) and \
                            (y <= self.lato//2 + 1 and \
                            y >= self.lato//2 + 1):
                            risultato += 0.25

                    elif self.damiera[x][y] == EnumPedine.PEDINA_NERA:
                        risultato -= 1

                    elif self.damiera[x][y] == EnumPedine.DAMA_NERA:
                        risultato -= 2

                elif self.turno == EnumTurno.NERO:
                    if self.damiera[x][y] == EnumPedine.PEDINA_NERA:
                        risultato += 1

                        if (y == 0 or y == self.lato-1) and (x == 0 or \
                            x == self.lato-1):
                            risultato += 0.5

                        elif (x <= self.lato//2 + 1 and \
                            x >= self.lato//2 + 1) and \
                            (y <= self.lato//2 + 1 and \
                            y >= self.lato//2 + 1):
                            risultato += 0.25

                    elif self.damiera[x][y] == EnumPedine.DAMA_NERA:
                        risultato += 3

                        if (y == 0 or y == self.lato-1) and (x == 0 or \
                            x == self.lato-1):
                            risultato += 0.5

                        elif (x <= self.lato//2 + 1 and \
                            x >= self.lato//2 + 1) and \
                            (y <= self.lato//2 + 1 and \
                            y >= self.lato//2 + 1):
                            risultato += 0.25

                    elif self.damiera[x][y] == EnumPedine.PEDINA_BIANCA:
                        risultato -= 1

                    elif self.damiera[x][y] == EnumPedine.DAMA_BIANCA:
                        risultato -= 2

        return risultato



    def valuta_mossa(self, mossa, turno):
        risultato_attuale = self.calcola_punteggio(turno)

        damiera = Damiera(self.lato, self.euristica, copy.deepcopy(self.damiera), turno, self.selezionato)

        damiera.muovi(mossa)

        risultato_successivo = damiera.calcola_punteggio(turno)

        return risultato_successivo - risultato_attuale



    def calcola_mosse_consentite(self):
        mosse_consentite = list()
        
        for x in range(self.lato):
            for y in range(self.lato):
                if self.turno == EnumTurno.BIANCO and \
                    (self.damiera[x][y] == EnumPedine.PEDINA_BIANCA or \
                    self.damiera[x][y] == EnumPedine.DAMA_BIANCA):
                    mosse_consentite += self.calcola_mosse_pedina((x, y))
                
                elif self.turno == EnumTurno.NERO and \
                    (self.damiera[x][y] == EnumPedine.PEDINA_NERA or \
                     self.damiera[x][y] == EnumPedine.DAMA_NERA):
                    mosse_consentite += self.calcola_mosse_pedina((x, y))

        return mosse_consentite



    def calcola_mossa_migliore(self):

        if self.euristica == "MM":
            self.minimax(None, self.profondita, True)

        elif self.euristica == "AB":
            self.alpha_beta(None, self.profondita, float("-inf"),
                            float("inf"), self.turno)

        return self.mossa_ai



    def alpha_beta(self, nodo, profondita, alpha, beta, turno):
        
        if profondita == 0:
            self.mossa_ai = nodo
            return self.valuta_mossa(nodo, turno)

        mosse_consentite = self.calcola_mosse_consentite()

        if turno == self.turno:
            risultato = float("-inf")

            for mossa in mosse_consentite:
                risultato = max(risultato, self.alpha_beta(mossa, profondita-1, 
                                                        alpha, beta, False))
                alpha = max(alpha, risultato)

                if beta <= alpha:
                    break

        else:
            risultato = float("inf")

            for mossa in mosse_consentite:
                risultato = min(risultato, self.alpha_beta(mossa, profondita-1, 
                                                        alpha, beta, True))
                beta = min(beta, risultato)

                if beta <= alpha:
                    break

        return risultato



    def minimax(self, nodo, profondita, massimizza):
        
        if profondita == 0:
            self.mossa_ai = nodo
            return self.valuta_mossa(nodo, self.turno)
        
        mosse_consentite = self.calcola_mosse_consentite()

        if massimizza == True:
            risultato = float("-inf")

            for mossa in mosse_consentite:
                valore = self.minimax(mossa, profondita-1, False)

                risultato = max(risultato, valore)

            return risultato

        else:
            risultato = float("inf")

            for mossa in mosse_consentite:
                valore = self.minimax(mossa, profondita-1, True)
                
                risultato = min(risultato, valore)
            
            return risultato



    def muovi(self, mossa):
        x = mossa.inizio[0]
        y = mossa.inizio[1]

        pedina = self.damiera[x][y]

        self.damiera[x][y] = EnumPedine.VUOTO

        x = mossa.fine[0]
        y = mossa.fine[1]

        self.damiera[x][y] = pedina

        if mossa.pedina_mangiata is not None:
            x = mossa.pedina_mangiata[0]
            y = mossa.pedina_mangiata[1]

            self.damiera[x][y] = EnumPedine.VUOTO



    def calcola_pedine(self):
        n = 0

        for x in range(self.lato):
            for y in range(self.lato):
                if self.damiera[x][y] != EnumPedine.VUOTO:
                    n += 1

        return n



    def calcola_pedine_nere(self):
        n = 0
        
        for x in range(self.lato):
            for y in range(self.lato):
                if self.damiera[x][y] == EnumPedine.PEDINA_NERA or \
                    self.damiera[x][y] == EnumPedine.DAMA_NERA:
                    n += 1
        
        return n



    def calcola_pedine_bianche(self):
        n = 0
        
        for x in range(self.lato):
            for y in range(self.lato):
                if self.damiera[x][y] == EnumPedine.PEDINA_BIANCA or \
                    self.damiera[x][y] == EnumPedine.DAMA_BIANCA:
                    n += 1
        
        return n



    def cambia_turno(self):

        for x in range(self.lato):
            if self.damiera[x][0] == EnumPedine.PEDINA_NERA:
                self.damiera[x][0] = EnumPedine.DAMA_NERA

        for x in range(self.lato):
            if self.damiera[x][self.lato-1] == EnumPedine.PEDINA_BIANCA:
                self.damiera[x][self.lato-1] = EnumPedine.DAMA_BIANCA

        self.turno = (EnumTurno)(1 - self.turno)



def __str__(self):

    stringa = str()

    for x in range(self.lato):
        for y in range(self.lato):
            if self.damiera[y][x] == EnumPedine.PEDINA_BIANCA:
                stringa += "B "
            elif self.damiera[y][x] == EnumPedine.PEDINA_NERA:
                stringa += "N "
            else:
                stringa += "  "
        stringa += "\n"

    return stringa
