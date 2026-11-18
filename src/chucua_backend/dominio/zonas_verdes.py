from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class ZonaVerde(EntidadGeografica):
    """Parque o zona verde del barrio."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        area_aprox_m2,
        tipo_vegetacion,
        estado_mantenimiento,
        direccion,
        osm_id=None,
        id=None,
    ):
        self.area_aprox_m2 = area_aprox_m2
        self.tipo_vegetacion = tipo_vegetacion
        self.estado_mantenimiento = estado_mantenimiento
        self.direccion = direccion
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Una zona verde debe ser un punto")
        try:
            area = float(self.area_aprox_m2)
        except (TypeError, ValueError) as exc:
            raise ErrorValidacion("El área debe ser un número en metros cuadrados") from exc
        if area <= 0:
            raise ErrorValidacion("El área de la zona verde debe ser mayor que cero")
        self.area_aprox_m2 = area
        self.tipo_vegetacion = texto_obligatorio(
            self.tipo_vegetacion, "tipo_vegetacion"
        )
        self.estado_mantenimiento = texto_obligatorio(
            self.estado_mantenimiento, "estado_mantenimiento"
        )
        self.direccion = texto_obligatorio(self.direccion, "direccion")

    def propiedades(self) -> dict:
        return {
            "area_aprox_m2": self.area_aprox_m2,
            "tipo_vegetacion": self.tipo_vegetacion,
            "estado_mantenimiento": self.estado_mantenimiento,
            "direccion": self.direccion,
        }
