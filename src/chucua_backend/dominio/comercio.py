from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class ComercioLocal(EntidadGeografica):
    """Establecimiento comercial del barrio."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        categoria_comercial,
        nombre_establecimiento,
        direccion,
        horario,
        osm_id=None,
        id=None,
    ):
        self.categoria_comercial = categoria_comercial
        self.nombre_establecimiento = nombre_establecimiento
        self.direccion = direccion
        self.horario = horario
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un comercio local debe ser un punto")
        self.categoria_comercial = texto_obligatorio(
            self.categoria_comercial, "categoria_comercial"
        )
        self.nombre_establecimiento = texto_obligatorio(
            self.nombre_establecimiento, "nombre_establecimiento"
        )
        self.direccion = texto_obligatorio(self.direccion, "direccion")
        self.horario = texto_obligatorio(self.horario, "horario")

    def propiedades(self) -> dict:
        return {
            "categoria_comercial": self.categoria_comercial,
            "nombre_establecimiento": self.nombre_establecimiento,
            "direccion": self.direccion,
            "horario": self.horario,
        }
