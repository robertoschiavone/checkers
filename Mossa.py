class Mossa:

    def __init__(self, inizio, fine, pedina_mangiata=None):
        self.inizio = inizio
        self.fine = fine

        self.pedina_mangiata = pedina_mangiata

    def __str__(self):
        string = "(" + str(self.inizio[0]) + ", " + str(self.inizio[1]) + ") "
        string += "-> (" + str(self.fine[0]) + ", " + str(self.fine[1]) + ")"

        return string
