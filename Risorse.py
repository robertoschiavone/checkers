import pyglet

class Risorse:
    """
    Gestisce il caricamento di tutte le immagini utilizzate per la corretta
    visualizzazione della damiera e delle pedine.
    """

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
        """
        Restituisce l'immagine della casella bianca.
        """
        return self.casella_bianca

    def leggi_casella_nera(self):
        """
        Restituisce l'immagine della casella nera.
        """
        return self.casella_nera

    def leggi_casella_selezionata(self):
        """
        Restituisce l'immagine della casella selezionata.
        """
        return self.casella_selezionata

    def leggi_casella_evidenziata(self):
        """
        Restituisce l'immagine della casella evidenziata.
        """
        return self.casella_evidenziata

    def leggi_pedina_bianca(self):
        """
        Restituisce l'immagine della pedina bianca.
        """
        return self.pedina_bianca

    def leggi_pedina_nera(self):
        """
        Restituisce l'immagine della pedina bianca.
        """
        return self.pedina_nera

    def leggi_dama_bianca(self):
        """
        Restituisce l'immagine della dama bianca
        """
        return self.dama_bianca

    def leggi_dama_nera(self):
        """
        Restituisce l'immagine della dama bianca
        """
        return self.dama_nera

    def leggi_vuoto(self):
        """
        Restituisce l'immagine vuota
        """
        return self.vuoto
