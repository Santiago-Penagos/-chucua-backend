from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class CentroSalud(EntidadGeografica):
    def __init__(self, *, nombre, sector, geometria, tipo_centro, nivel_atencion, horario, direccion, osm_id=None, id=None):
        self.tipo_centro = tipo_centro
        self.nivel_atencion = nivel_atencion
        self.horario = horario
        self.direccion = direccion
        super().__init__(nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id)

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un centro de salud debe ser un punto")
        self.tipo_centro = texto_obligatorio(self.tipo_centro, "tipo_centro")
        self.nivel_atencion = texto_obligatorio(self.nivel_atencion, "nivel_atencion")
        self.horario = texto_obligatorio(self.horario, "horario")
        self.direccion = texto_obligatorio(self.direccion, "direccion")

    def propiedades(self) -> dict:
        return {
            "tipo_centro": self.tipo_centro,
            "nivel_atencion": self.nivel_atencion,
            "horario": self.horario,
            "direccion": self.direccion,
        }
