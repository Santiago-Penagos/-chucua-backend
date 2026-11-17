from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class CentroEducativo(EntidadGeografica):
    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        nivel_educativo,
        naturaleza,
        osm_id=None,
        id=None,
    ):
        self.nivel_educativo = nivel_educativo
        self.naturaleza = naturaleza
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un centro educativo debe ser un punto")
        self.nivel_educativo = texto_obligatorio(
            self.nivel_educativo, "nivel_educativo"
        )
        self.naturaleza = texto_obligatorio(self.naturaleza, "naturaleza")

    def propiedades(self) -> dict:
        return {
            "nivel_educativo": self.nivel_educativo,
            "naturaleza": self.naturaleza,
        }
