from ..errores import ErrorValidacion
from .geometria import Linea, Punto, Poligono


def desde_geojson(datos: dict):
    """Convierte una geometría GeoJSON en un objeto de valor del dominio."""
    if not isinstance(datos, dict):
        raise ErrorValidacion("La geometría debe ser un objeto GeoJSON")
    tipo = datos.get("type")
    coords = datos.get("coordinates")
    if tipo == "Point":
        return Punto(tuple(coords))
    if tipo == "LineString":
        return Linea(tuple(tuple(c) for c in coords))
    if tipo == "Polygon":
        if not coords or not coords[0]:
            raise ErrorValidacion("El polígono no tiene anillo exterior")
        return Poligono(tuple(tuple(c) for c in coords[0]))
    raise ErrorValidacion(f"Tipo de geometría no soportado: {tipo!r}")
