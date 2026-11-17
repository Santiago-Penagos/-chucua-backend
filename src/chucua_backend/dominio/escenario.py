from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class EscenarioDeportivo(EntidadGeografica):
    def __init__(self, *, nombre, sector, geometria, tipo_escenario, osm_id=None, id=None):
        self.tipo_escenario = tipo_escenario
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un escenario deportivo debe ser un punto")
        self.tipo_escenario = texto_obligatorio(self.tipo_escenario, "tipo_escenario")

    def propiedades(self) -> dict:
        return {"tipo_escenario": self.tipo_escenario}
