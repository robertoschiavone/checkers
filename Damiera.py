from EnumPedine import *
from EnumTurno import *
from Mossa import *
from Risorse import *

import copy
import pyglet

class Damiera:

    def __init__(self, lato, euristica="AB", pedine=[], turno_iniziale = EnumTurno.BIANCO, selezionato=None):
        """
        Inizializza la damiera,, creando le opportune strutture i dati per 
        gestire le pedine, le caselle e la logica di gioco

        Parametri:
            - impostazioni: oggetto contenente le informazioni di altezza e
            larghezza, necessarie per la corretta inizializzazione della damiera
        """

        self.euristica = euristica
        
        self.turno = EnumTurno.BIANCO
        self.turno_iniziale = turno_iniziale

        self.lato = lato

        self.selezionato = selezionato

        self.mossa_ai = None

        self.conta_turno = 0

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
            
                else:
                    pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_vuoto())

                pedine[x][y].position = (x * 64, y * 64)
                pedine[x][y].batch = batch_pedine

        batch_caselle.draw()
        batch_pedine.draw()



    def calcola_mosse_pedina(self, pedina):

        print(pedina)

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

            if self.leggi_pedina(x, y) \
                == EnumPedine.DAMA_NERA:
                pass

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
                pass

        print(self.turno)
        print(len(mosse_consentite))
        return mosse_consentite



    def calcola_punteggio(self, turno):
        
        risultato = 0

        for x in range(self.lato):
            for y in range(self.lato):
                if self.turno == EnumTurno.BIANCO:
                    if self.damiera[x][y] == EnumPedine.PEDINA_BIANCA:
                        risultato += 1
                    elif self.damiera[x][y] == EnumPedine.DAMA_BIANCA:
                        risultato += 2
                    elif self.damiera[x][y] == EnumPedine.PEDINA_NERA:
                        risultato -= 1
                    elif self.damiera[x][y] == EnumPedine.DAMA_NERA:
                        risultato -= 2

                elif self.turno == EnumTurno.NERO:
                    if self.damiera[x][y] == EnumPedine.PEDINA_NERA:
                        risultato += 1
                    elif self.damiera[x][y] == EnumPedine.DAMA_NERA:
                        risultato += 2
                    elif self.damiera[x][y] == EnumPedine.PEDINA_BIANCA:
                        risultato -= 1
                    elif self.damiera[x][y] == EnumPedine.DAMA_BIANCA:
                        risultato -= 2

        return risultato



    def valuta_mossa(self, mossa, turno):
        risultato_attuale = self.calcola_punteggio(turno)

        damiera = Damiera(self.lato, copy.deepcopy(self.damiera), self.turno, self.selezionato)

        damiera.muovi(mossa)

        risultato_successivo = damiera.calcola_punteggio(turno)

        return risultato_successivo - risultato_attuale



    def calcola_mosse_consentite(self):
        mosse_consentite = list()
        
        for x in range(self.lato):
            for y in range(self.lato):
                if self.turno == EnumTurno.BIANCO and \
                    self.damiera[x][y] == EnumPedine.PEDINA_BIANCA:
                    mosse_consentite += self.calcola_mosse_pedina((x, y))
                
                elif self.turno == EnumTurno.NERO and \
                    self.damiera[x][y] == EnumPedine.PEDINA_NERA:
                    mosse_consentite += self.calcola_mosse_pedina((x, y))
        
        return mosse_consentite

    def calcola_mossa_migliore(self):

        if self.euristica == "MM":
            self.minimax(None, 4, True)

        elif self.euristica == "AB":
            self.alpha_beta(None, 4, float("-inf"),
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

                temp_risultato = risultato
                risultato = max(risultato, valore)

                if risultato != temp_risultato:
                    self.mossa_ai = nodo

            return risultato

        else:
            risultato = float("inf")

            for mossa in mosse_consentite:
                valore = self.minimax(mossa, profondita-1, True)
                
                temp_risultato = risultato
                risultato = min(risultato, valore)

                if risultato != temp_risultato:
                    self.mossa_ai = nodo
            
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

    def cambia_turno(self):
        self.turno = (EnumTurno)(1 - self.turno)
