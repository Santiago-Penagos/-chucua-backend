"""Polígonos reales del barrio Chucua de la Vaca y sus tres sectores."""

from ..dominio.geometria import Coordenada

SECTORES = ("I", "II", "III")

LIMITES_BARRIO = {
    "norte": 4.6318,
    "sur": 4.6238,
    "occidente": -74.1695,
    "oriente": -74.1615,
}

ORIENTE_NORTE = -74.1638
PENDIENTE_ORIENTE = (
    LIMITES_BARRIO["oriente"] - ORIENTE_NORTE
) / (LIMITES_BARRIO["sur"] - LIMITES_BARRIO["norte"])

BANDAS_SECTOR = {
    "I": (4.6292, 4.6318),
    "II": (4.6265, 4.6292),
    "III": (4.6238, 4.6265),
}


def longitud_oriente(latitud: float) -> float:
    """Longitud del eje de la Av. Agoberto Mejía / Carrera 80."""
    return ORIENTE_NORTE + (latitud - LIMITES_BARRIO["norte"]) * PENDIENTE_ORIENTE


def _anillo(sur: float, norte: float) -> tuple[Coordenada, ...]:
    occidente = LIMITES_BARRIO["occidente"]
    return (
        (occidente, sur),
        (longitud_oriente(sur), sur),
        (longitud_oriente(norte), norte),
        (occidente, norte),
        (occidente, sur),
    )


POLIGONO_BARRIO = _anillo(LIMITES_BARRIO["sur"], LIMITES_BARRIO["norte"])

ANILLOS: dict[str, tuple[Coordenada, ...]] = {
    sector: _anillo(*BANDAS_SECTOR[sector]) for sector in SECTORES
}

NOMBRES = {
    "I": "Sector I - Ronda Norte del Humedal La Vaca",
    "II": "Sector II - Equipamientos y Calle 42 Sur",
    "III": "Sector III - Parques Vecinales y Ronda Sur",
}

DESCRIPCIONES = {
    "I": "Entre la Calle 38C Sur, el borde sur de Corabastos y la ronda norte del humedal.",
    "II": "Zona central sobre el eje Calle 41F Sur / Calle 42 Sur y las carreras 81A a 84.",
    "III": "Zona sur entre la Calle 42F Sur y la ronda sur del Humedal La Vaca.",
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
