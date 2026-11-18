from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class PuntoHumedal(EntidadGeografica):
    """Punto de interés ecológico dentro del Humedal La Vaca."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        zona_humedal,
        estado_conservacion,
        especie_destacada,
        osm_id=None,
        id=None,
    ):
        self.zona_humedal = zona_humedal
        self.estado_conservacion = estado_conservacion
        self.especie_destacada = especie_destacada
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un punto del humedal debe ser un punto")
        self.zona_humedal = texto_obligatorio(self.zona_humedal, "zona_humedal")
        self.estado_conservacion = texto_obligatorio(
            self.estado_conservacion, "estado_conservacion"
        )
        self.especie_destacada = texto_obligatorio(
            self.especie_destacada, "especie_destacada"
        )

    def propiedades(self) -> dict:
        return {
            "zona_humedal": self.zona_humedal,
            "estado_conservacion": self.estado_conservacion,
            "especie_destacada": self.especie_destacada,
        }
