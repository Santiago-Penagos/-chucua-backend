from chucua_backend.dominio.geometria import Coordenada

LIMITE_I_II = -74.166667
LIMITE_II_III = -74.162833


def clasificar_sector(longitud: float) -> str:
    """Clasifica una longitud en tercios oeste, central y este del bbox."""
    if longitud < LIMITE_I_II:
        return "I"
    if longitud <= LIMITE_II_III:
        return "II"
    return "III"


def sector_de_coordenadas(coordenadas: list[Coordenada]) -> str:
    if not coordenadas:
        raise ValueError("No hay coordenadas para clasificar")
    longitud = sum(c[0] for c in coordenadas) / len(coordenadas)
    return clasificar_sector(longitud)
