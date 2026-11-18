from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class ParaderoSitp(EntidadGeografica):
    """Paradero del Sistema Integrado de Transporte Público."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        codigo_paradero,
        rutas_alimentadoras,
        direccion,
        estado_senalizacion,
        osm_id=None,
        id=None,
    ):
        self.codigo_paradero = codigo_paradero
        self.rutas_alimentadoras = rutas_alimentadoras
        self.direccion = direccion
        self.estado_senalizacion = estado_senalizacion
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un paradero SITP debe ser un punto")
        self.codigo_paradero = texto_obligatorio(
            self.codigo_paradero, "codigo_paradero"
        )
        self.rutas_alimentadoras = texto_obligatorio(
            self.rutas_alimentadoras, "rutas_alimentadoras"
        )
        self.direccion = texto_obligatorio(self.direccion, "direccion")
        self.estado_senalizacion = texto_obligatorio(
            self.estado_senalizacion, "estado_senalizacion"
        )

    def propiedades(self) -> dict:
        return {
            "codigo_paradero": self.codigo_paradero,
            "rutas_alimentadoras": self.rutas_alimentadoras,
            "direccion": self.direccion,
            "estado_senalizacion": self.estado_senalizacion,
        }
