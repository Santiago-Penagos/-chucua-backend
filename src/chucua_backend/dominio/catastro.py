from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Poligono


class InformacionCatastral(EntidadGeografica):
    def __init__(
        self, *, nombre, sector, geometria, uso_suelo, area_m2, osm_id=None, id=None
    ):
        self.uso_suelo = uso_suelo
        self.area_m2 = area_m2
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Poligono):
            raise ErrorValidacion("La información catastral debe ser un polígono")
        self.uso_suelo = texto_obligatorio(self.uso_suelo, "uso_suelo")
        try:
            area = float(self.area_m2)
        except (TypeError, ValueError) as exc:
            raise ErrorValidacion("El área debe ser un número en metros cuadrados") from exc
        if area <= 0:
            raise ErrorValidacion("El área catastral debe ser mayor que cero")
        self.area_m2 = area

    def propiedades(self) -> dict:
        return {"uso_suelo": self.uso_suelo, "area_m2": self.area_m2}
