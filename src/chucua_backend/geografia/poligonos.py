"""Polígonos oficiales IDECA/UAECD del barrio Chucua de la Vaca (Sectores I, II y III)."""

from importlib.resources import files
import json

from ..dominio.geometria import Coordenada

SECTORES = ("I", "II", "III")


def _cargar_oficial() -> dict:
    recurso = files("seed").joinpath("datos/sectores_barrio.geojson")
    return json.loads(recurso.read_text(encoding="utf-8"))


_COLECCION = _cargar_oficial()

ANILLOS: dict[str, tuple[Coordenada, ...]] = {
    feat["properties"]["sector"]: tuple(
        (float(lon), float(lat)) for lon, lat in feat["geometry"]["coordinates"]
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
    "norte": max(p for p in _TODOS),
    "sur": min(p for p in _TODOS),
    "occidente": min(p for p in _TODOS),
    "oriente": max(p for p in _TODOS),
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
