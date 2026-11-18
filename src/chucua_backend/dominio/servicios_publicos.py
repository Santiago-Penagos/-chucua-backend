from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class PuntoServicioPublico(EntidadGeografica):
    """Infraestructura de servicios públicos del barrio."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        tipo_servicio,
        estado_operativo,
        ubicacion_referencia,
        osm_id=None,
        id=None,
    ):
        self.tipo_servicio = tipo_servicio
        self.estado_operativo = estado_operativo
        self.ubicacion_referencia = ubicacion_referencia
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un punto de servicios públicos debe ser un punto")
        self.tipo_servicio = texto_obligatorio(self.tipo_servicio, "tipo_servicio")
        self.estado_operativo = texto_obligatorio(
            self.estado_operativo, "estado_operativo"
        )
        self.ubicacion_referencia = texto_obligatorio(
            self.ubicacion_referencia, "ubicacion_referencia"
        )

    def propiedades(self) -> dict:
        return {
            "tipo_servicio": self.tipo_servicio,
            "estado_operativo": self.estado_operativo,
            "ubicacion_referencia": self.ubicacion_referencia,
        }
