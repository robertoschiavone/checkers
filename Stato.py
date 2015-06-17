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

from Turno import *

class Stato:

    def __init__(self, turno, selezionato = None):
        self.turno = turno

        self.selezionato = selezionato

    def cambia_turno(self):
        t = EnumTurno()

        if self.turno == t.leggi_nero():
            self.turno = t.leggi_bianco()
        else:
            self.turno = t.leggi_nero()

    def leggi_turno(self):
        return self.turno

    def scrivi_turno(self, selected):
        self.selezionato

    def leggi_selezionato(self):
        return self.selezionato
