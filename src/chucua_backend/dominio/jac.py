from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class JuntaAccionComunal(EntidadGeografica):
    def __init__(self, *, nombre, sector, geometria, presidente_contacto, direccion, horario_atencion, osm_id=None, id=None):
        self.presidente_contacto = presidente_contacto
        self.direccion = direccion
        self.horario_atencion = horario_atencion
        super().__init__(nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id)

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Una JAC debe ser un punto")
        self.presidente_contacto = texto_obligatorio(self.presidente_contacto, "presidente_contacto")
        self.direccion = texto_obligatorio(self.direccion, "direccion")
        self.horario_atencion = texto_obligatorio(self.horario_atencion, "horario_atencion")

    def propiedades(self) -> dict:
        return {
            "presidente_contacto": self.presidente_contacto,
            "direccion": self.direccion,
            "horario_atencion": self.horario_atencion,
        }
