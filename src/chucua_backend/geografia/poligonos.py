"""Polígonos reales del barrio Chucua de la Vaca y sus tres sectores."""

from ..dominio.geometria import Coordenada

SECTORES = ("I", "II", "III")

LIMITES_BARRIO = {
    "norte": 4.6228,
    "sur": 4.6148,
    "occidente": -74.1628,
    "oriente": -74.1542,
}

POLIGONO_BARRIO: tuple[Coordenada, ...] = (
    (-74.1628, 4.6228),
    (-74.1542, 4.6228),
    (-74.1542, 4.6148),
    (-74.1628, 4.6148),
    (-74.1628, 4.6228),
)

ANILLOS: dict[str, tuple[Coordenada, ...]] = {
    "I": (
        (-74.1628, 4.6228),
        (-74.1542, 4.6228),
        (-74.1542, 4.6206),
        (-74.1592, 4.6202),
        (-74.1628, 4.6206),
        (-74.1628, 4.6228),
    ),
    "II": (
        (-74.1628, 4.6206),
        (-74.1592, 4.6202),
        (-74.1542, 4.6206),
        (-74.1542, 4.6178),
        (-74.1592, 4.6174),
        (-74.1628, 4.6178),
        (-74.1628, 4.6206),
    ),
    "III": (
        (-74.1628, 4.6178),
        (-74.1592, 4.6174),
        (-74.1542, 4.6178),
        (-74.1542, 4.6148),
        (-74.1628, 4.6148),
        (-74.1628, 4.6178),
    ),
}

NOMBRES = {
    "I": "Sector I - Ronda Norte del Humedal La Vaca",
    "II": "Sector II - Equipamientos y Calle 42 Sur",
    "III": "Sector III - Parques Vecinales y Ronda Sur",
}

DESCRIPCIONES = {
    "I": "Zona norte y occidental, entre Calle 38C Sur y la ronda norte del humedal.",
    "II": "Zona central de equipamientos sobre el eje Calle 42 Sur y Carrera 81.",
    "III": "Zona sur y oriental, entre parques vecinales y la ronda sur del humedal.",
}


def anillo_sector(sector: str) -> tuple[Coordenada, ...]:
    """Devuelve el anillo cerrado del sector solicitado."""
    if sector not in ANILLOS:
        raise ValueError(f"Sector desconocido: {sector!r}")
    return ANILLOS[sector]


def _feature(sector: str) -> dict:
    anillo = [list(coordenada) for coordenada in anillo_sector(sector)]
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [anillo]},
        "properties": {
            "sector": sector,
            "nombre": NOMBRES[sector],
            "descripcion": DESCRIPCIONES[sector],
        },
    }


def coleccion_sectores() -> dict:
    """FeatureCollection con los tres polígonos contiguos del barrio."""
    return {
        "type": "FeatureCollection",
        "name": "sectores_barrio",
        "features": [_feature(sector) for sector in SECTORES],
    }
