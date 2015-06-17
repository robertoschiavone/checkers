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

import pyglet

class Risorse:
    
    def __init__(self):
        self.casella_bianca = pyglet.image.load("immagini/casella_bianca.png")
        self.casella_nera = pyglet.image.load("immagini/casella_nera.png")
        
        self.casella_selezionata = pyglet.image.load("immagini/casella_selezionata.png")
        
        self.casella_evidenziata = pyglet.image.load("immagini/casella_evidenziata.png")

        self.pedina_bianca = pyglet.image.load("immagini/pedina_bianca.png")
        self.pedina_nera = pyglet.image.load("immagini/pedina_nera.png")
        
        self.dama_bianca = pyglet.image.load("immagini/dama_bianca.png")
        self.dama_nera = pyglet.image.load("immagini/dama_nera.png")

        self.vuoto = pyglet.image.load("immagini/nessuna_pedina.png")

    def leggi_casella_bianca(self):
        return self.casella_bianca

    def leggi_casella_nera(self):
        return self.casella_nera

    def leggi_casella_selezionata(self):
        return self.casella_selezionata

    def leggi_casella_evidenziata(self):
        return self.casella_evidenziata

    def leggi_pedina_bianca(self):
        return self.pedina_bianca

    def leggi_pedina_nera(self):
        return self.pedina_nera

    def leggi_dama_bianca(self):
        return self.dama_bianca

    def leggi_dama_nera(self):
        return self.dama_nera

    def leggi_vuoto(self):
        return self.vuoto
