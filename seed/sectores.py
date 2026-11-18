import json
from pathlib import Path

from chucua_backend.dominio.geometria import Coordenada
from chucua_backend.errores import ErrorValidacion
from chucua_backend.geografia import (
    ANILLOS as POLIGONOS,
    SECTORES,
    clasificar_punto,
    coleccion_sectores,
    dentro_del_barrio,
)

RUTA_GEOJSON = Path(__file__).resolve().parent / "datos" / "sectores_barrio.geojson"


def clasificar_sector(longitud: float, latitud: float) -> str:
    """Ubica una coordenada en el sector real I, II o III del barrio."""
    return clasificar_punto(longitud, latitud)


def sector_de_coordenadas(coordenadas: list[Coordenada]) -> str:
    if not coordenadas:
        raise ValueError("No hay coordenadas para clasificar")
    for longitud, latitud in coordenadas:
        if not dentro_del_barrio(longitud, latitud):
            raise ErrorValidacion("La geometría sale de Chucua de la Vaca")
    longitud = sum(c[0] for c in coordenadas) / len(coordenadas)
    latitud = sum(c[1] for c in coordenadas) / len(coordenadas)
    return clasificar_sector(longitud, latitud)


def exportar_geojson(ruta: Path = RUTA_GEOJSON) -> Path:
    """Escribe el FeatureCollection de sectores con una línea por polígono."""
    coleccion = coleccion_sectores()
    features = [
        "    " + json.dumps(feature, ensure_ascii=False) + ","
        for feature in coleccion["features"]
    ]
    features[-1] = features[-1].rstrip(",")
    contenido = "\n".join(
        [
            "{",
            '  "type": "FeatureCollection",',
            '  "name": "sectores_barrio",',
            '  "features": [',
            *features,
            "  ]",
            "}",
            "",
        ]
    )
    ruta.write_text(contenido, encoding="utf-8")
    return ruta
