from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Linea


class EstadoVia(EntidadGeografica):
    def __init__(self, *, nombre, sector, geometria, tipo_via, estado, osm_id=None, id=None):
        self.tipo_via = tipo_via
        self.estado = estado
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Linea):
            raise ErrorValidacion("El estado de una vía debe ser una línea")
        self.tipo_via = texto_obligatorio(self.tipo_via, "tipo_via")
        self.estado = texto_obligatorio(self.estado, "estado")

    def propiedades(self) -> dict:
        return {"tipo_via": self.tipo_via, "estado": self.estado}
