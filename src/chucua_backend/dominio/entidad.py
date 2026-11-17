from abc import ABC, abstractmethod

from ..errores import ErrorValidacion
from .geometria import Coordenada
from .sector import Sector, validar_sector


def texto_obligatorio(valor: str, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorValidacion(f"El campo '{campo}' es obligatorio")
    return valor.strip()


class EntidadGeografica(ABC):
    """Base común de las entidades geográficas del barrio."""

    def __init__(self, *, nombre, sector, geometria, osm_id=None, id=None):
        self.id = id
        self.nombre = texto_obligatorio(nombre, "nombre")
        self.sector = validar_sector(sector)
        self.geometria = geometria
        self.osm_id = osm_id
        self.validar()

    @abstractmethod
    def validar(self) -> None:
        """Comprueba las invariantes propias del dominio."""

    @abstractmethod
    def propiedades(self) -> dict:
        """Atributos propios que viajan en GeoJSON."""

    def get_coordenadas(self) -> list[Coordenada]:
        return self.geometria.coordenadas

    def get_sector(self) -> Sector:
        return self.sector

    def a_geojson(self) -> dict:
        propiedades = {
            "id": self.id,
            "nombre": self.nombre,
            "sector": self.sector,
            "osm_id": self.osm_id,
            **self.propiedades(),
        }
        return {
            "type": "Feature",
            "geometry": self.geometria.a_geojson(),
            "properties": propiedades,
        }
