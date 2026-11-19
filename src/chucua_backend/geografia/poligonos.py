"""Polígonos oficiales IDECA/UAECD del barrio Chucua de la Vaca (Sectores I, II y III)."""

import json
from pathlib import Path

from ..dominio.geometria import Coordenada

SECTORES = ("I", "II", "III")

_DATOS = (
    Path(__file__).resolve().parents[3] / "seed" / "datos" / "sectores_barrio.geojson"
)


def _cargar_oficial() -> dict:
    return json.loads(_DATOS.read_text(encoding="utf-8"))


_COLECCION = _cargar_oficial()

ANILLOS: dict[str, tuple[Coordenada, ...]] = {
    feat["properties"]["sector"]: tuple(
        (float(lon), float(lat)) for lon, lat in feat["geometry"]["coordinates"][0]
    )
    for feat in _COLECCION["features"]
}

NOMBRES: dict[str, str] = {
    feat["properties"]["sector"]: feat["properties"]["nombre"]
    for feat in _COLECCION["features"]
}

DESCRIPCIONES: dict[str, str] = {
    feat["properties"]["sector"]: feat["properties"]["descripcion"]
    for feat in _COLECCION["features"]
}

_TODOS = [punto for anillo in ANILLOS.values() for punto in anillo]

LIMITES_BARRIO = {
    "norte": max(p[1] for p in _TODOS),
    "sur": min(p[1] for p in _TODOS),
    "occidente": min(p[0] for p in _TODOS),
    "oriente": max(p[0] for p in _TODOS),
}

POLIGONO_BARRIO: tuple[Coordenada, ...] = (
    (LIMITES_BARRIO["occidente"], LIMITES_BARRIO["sur"]),
    (LIMITES_BARRIO["oriente"], LIMITES_BARRIO["sur"]),
    (LIMITES_BARRIO["oriente"], LIMITES_BARRIO["norte"]),
    (LIMITES_BARRIO["occidente"], LIMITES_BARRIO["norte"]),
    (LIMITES_BARRIO["occidente"], LIMITES_BARRIO["sur"]),
)


def anillo_sector(sector: str) -> tuple[Coordenada, ...]:
    """Devuelve el anillo cerrado del sector catastral oficial solicitado."""
    if sector not in ANILLOS:
        raise ValueError(f"Sector desconocido: {sector!r}")
    return ANILLOS[sector]


def coleccion_sectores() -> dict:
    """FeatureCollection oficial IDECA/UAECD con los tres sectores del barrio."""
    return _cargar_oficial()
