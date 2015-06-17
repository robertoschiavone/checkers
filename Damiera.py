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

from EnumPedine import *
from Risorse import *
from Impostazioni import *

import pyglet

class Damiera:

    def __init__(self, impostazioni):
        
        self.impostazioni = impostazioni

        larghezza = impostazioni.leggi_larghezza()
        altezza = impostazioni.leggi_altezza()

        self.batch_pedine = pyglet.graphics.Batch()
        self.batch_caselle = pyglet.graphics.Batch()

        risorse = Risorse()
    
        enum_pedine = EnumPedine()

        self.sfondo = [[None for x in range(altezza)] for x in range(larghezza)]

        for x in range(larghezza):
            for y in range(altezza):
                if (x + y) % 2 == 0:
                    self.sfondo[x][y] = pyglet.sprite.Sprite(risorse.leggi_casella_bianca())
                else:
                    self.sfondo[x][y] = pyglet.sprite.Sprite(risorse.leggi_casella_nera())

                self.sfondo[x][y].batch = self.batch_caselle
                self.sfondo[x][y].position = (x * 64, y * 64)
        
        self.logica_pedine = [[None for x in range(altezza)] for x in range(larghezza)]

        for x in range(larghezza):
            for y in range(altezza):

                if (x + y) % 2 != 0:
                    if y in range(3):
                        self.logica_pedine[x][y] = enum_pedine.leggi_pedina_bianca()
                    elif y in range(3, height):
                        if (x % 2) == 0:
                            self.logica_pedine[x][y] = enum_pedine.leggi_pedina_nera()
                        else:
                            self.logica_pedine[x][y] = enum_pedine.leggi_vuoto()
                    else:
                       self.logica_pedine[x][y] = enum_pedine.leggi_vuoto()
                else:
                    self.logica_pedine[x][y] = enum_pedine.leggi_vuoto()

        self.grafica_pedine = [[None for x in range(altezza)] for x in range(larghezza)]

        for x in range(larghezza):
            for y in range(altezza):

                if (x + y) % 2 != 0:
                    if y in range(3):
                        self.grafica_pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_pedina_bianca())
                    elif y in range(3, height):
                        if (x % 2) == 0:
                            self.grafica_pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_pedina_nera())
                        else:
                            self.grafica_pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_vuoto())
                    else:
                        self.grafica_pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_vuoto())
                else:
                    self.grafica_pedine[x][y] = pyglet.sprite.Sprite(risorse.leggi_vuoto())

                self.grafica_pedine[x][y].position = (x * 64, y * 64)
                self.grafica_pedine[x][y].batch = batch

    def leggi_pedina(self, x, y):
        return self.logica_pedine[x][y]

    def draw(self):
        self.batch_caselle.draw()
        self.batch_pedine.draw()
