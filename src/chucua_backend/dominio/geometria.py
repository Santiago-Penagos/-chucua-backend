from dataclasses import dataclass
from math import cos, radians

from ..errores import ErrorValidacion

Coordenada = tuple[float, float]


def _validar_coordenada(coord: Coordenada) -> Coordenada:
    if not isinstance(coord, (tuple, list)) or len(coord) != 2:
        raise ErrorValidacion("Cada coordenada debe tener longitud y latitud")
    try:
        lon, lat = float(coord[0]), float(coord[1])
    except (TypeError, ValueError) as exc:
        raise ErrorValidacion(f"Coordenada no numérica: {coord!r}") from exc
    if not -180 <= lon <= 180 or not -90 <= lat <= 90:
        raise ErrorValidacion(f"Coordenada fuera de rango: {coord!r}")
    return (lon, lat)


@dataclass(frozen=True)
class Punto:
    coordenada: Coordenada
    tipo = "Point"

    def __post_init__(self) -> None:
        object.__setattr__(self, "coordenada", _validar_coordenada(self.coordenada))

    @property
    def coordenadas(self) -> list[Coordenada]:
        return [self.coordenada]

    def a_geojson(self) -> dict:
        return {"type": self.tipo, "coordinates": list(self.coordenada)}


@dataclass(frozen=True)
class Linea:
    coordenadas: tuple[Coordenada, ...]
    tipo = "LineString"

    def __post_init__(self) -> None:
        valores = tuple(_validar_coordenada(c) for c in self.coordenadas)
        if len(valores) < 2:
            raise ErrorValidacion("Una línea requiere al menos dos coordenadas")
        object.__setattr__(self, "coordenadas", valores)

    def a_geojson(self) -> dict:
        return {"type": self.tipo, "coordinates": [list(c) for c in self.coordenadas]}


@dataclass(frozen=True)
class Poligono:
    coordenadas: tuple[Coordenada, ...]
    tipo = "Polygon"

    def __post_init__(self) -> None:
        valores = tuple(_validar_coordenada(c) for c in self.coordenadas)
        if len(set(valores)) < 3:
            raise ErrorValidacion("Un polígono requiere al menos tres vértices distintos")
        if valores[0] != valores[-1]:
            valores = valores + (valores[0],)
        object.__setattr__(self, "coordenadas", valores)

    def a_geojson(self) -> dict:
        anillo = [list(c) for c in self.coordenadas]
        return {"type": self.tipo, "coordinates": [anillo]}

    def area_m2(self) -> float:
        """Área aproximada en metros cuadrados (proyección local)."""
        anillo = self.coordenadas
        lat0 = sum(c[1] for c in anillo) / len(anillo)
        mx = 111320 * cos(radians(lat0))
        my = 110540
        suma = 0.0
        for (x1, y1), (x2, y2) in zip(anillo, anillo[1:]):
            suma += (x1 * mx) * (y2 * my) - (x2 * mx) * (y1 * my)
        return abs(suma) / 2
