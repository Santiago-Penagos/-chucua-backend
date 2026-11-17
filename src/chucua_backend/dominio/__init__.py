from .catastro import InformacionCatastral
from .educativo import CentroEducativo
from .entidad import EntidadGeografica
from .escenario import EscenarioDeportivo
from .geometria import Coordenada, Linea, Poligono, Punto
from .via import EstadoVia

__all__ = [
    "EntidadGeografica",
    "EscenarioDeportivo",
    "CentroEducativo",
    "EstadoVia",
    "InformacionCatastral",
    "Coordenada",
    "Punto",
    "Linea",
    "Poligono",
]
