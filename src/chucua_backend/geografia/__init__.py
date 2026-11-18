"""Delimitación geográfica oficial del barrio Chucua de la Vaca."""

from .clasificacion import (
    clasificar_punto,
    contiene_punto,
    dentro_del_barrio,
)
from .poligonos import (
    ANILLOS,
    DESCRIPCIONES,
    LIMITES_BARRIO,
    NOMBRES,
    POLIGONO_BARRIO,
    SECTORES,
    anillo_sector,
    coleccion_sectores,
)

__all__ = [
    "ANILLOS",
    "DESCRIPCIONES",
    "LIMITES_BARRIO",
    "NOMBRES",
    "POLIGONO_BARRIO",
    "SECTORES",
    "anillo_sector",
    "clasificar_punto",
    "coleccion_sectores",
    "contiene_punto",
    "dentro_del_barrio",
]
