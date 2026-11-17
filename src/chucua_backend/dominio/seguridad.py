from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class PuntoSeguridad(EntidadGeografica):
    def __init__(self, *, nombre, sector, geometria, tipo_punto, cuadrante, telefono_contacto, osm_id=None, id=None):
        self.tipo_punto = tipo_punto
        self.cuadrante = cuadrante
        self.telefono_contacto = telefono_contacto
        super().__init__(nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id)

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un punto de seguridad debe ser un punto")
        self.tipo_punto = texto_obligatorio(self.tipo_punto, "tipo_punto")
        self.cuadrante = texto_obligatorio(self.cuadrante, "cuadrante")
        self.telefono_contacto = texto_obligatorio(self.telefono_contacto, "telefono_contacto")

    def propiedades(self) -> dict:
        return {
            "tipo_punto": self.tipo_punto,
            "cuadrante": self.cuadrante,
            "telefono_contacto": self.telefono_contacto,
        }
