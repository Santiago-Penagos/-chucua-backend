"""Clasificación de coordenadas dentro de los polígonos reales del barrio."""

from ..errores import ErrorValidacion
from .poligonos import ANILLOS, LIMITES_BARRIO, SECTORES


def _dentro_de_anillo(anillo, longitud: float, latitud: float) -> bool:
    """Aplicación del algoritmo de ray casting a un anillo cerrado."""
    dentro = False
    for (x1, y1), (x2, y2) in zip(anillo, anillo[1:]):
        if (y1 > latitud) != (y2 > latitud):
            cruce = x1 + (latitud - y1) * (x2 - x1) / (y2 - y1)
            if longitud < cruce:
                dentro = not dentro
    return dentro


def contiene_punto(sector: str, longitud: float, latitud: float) -> bool:
    """Indica si una coordenada pertenece al polígono de un sector."""
    return _dentro_de_anillo(ANILLOS[sector], longitud, latitud)


def dentro_del_barrio(longitud: float, latitud: float) -> bool:
    """Comprueba que la coordenada esté dentro del barrio, sin importar el sector."""
    return any(contiene_punto(sector, longitud, latitud) for sector in SECTORES)


def clasificar_punto(longitud: float, latitud: float) -> str:
    """Devuelve el sector que contiene la coordenada o falla si está por fuera."""
    for sector in SECTORES:
        if contiene_punto(sector, longitud, latitud):
            return sector
    limites = ", ".join(f"{clave}={valor}" for clave, valor in LIMITES_BARRIO.items())
    raise ErrorValidacion(
        f"La coordenada ({longitud}, {latitud}) está fuera de Chucua de la Vaca "
        f"({limites})"
    )
