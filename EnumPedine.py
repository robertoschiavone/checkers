import enum

@enum.unique
class EnumPedine(enum.IntEnum):

    VUOTO = -1

    PEDINA_BIANCA = 0
    PEDINA_NERA = 1
    
    DAMA_BIANCA = 2
    DAMA_NERA = 3
