from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class EspacioCultural(EntidadGeografica):
    """Centro cultural o espacio de culto del barrio."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        tipo_espacio,
        actividad_principal,
        direccion,
        aforo_aproximado,
        osm_id=None,
        id=None,
    ):
        self.tipo_espacio = tipo_espacio
        self.actividad_principal = actividad_principal
        self.direccion = direccion
        self.aforo_aproximado = aforo_aproximado
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un espacio cultural debe ser un punto")
        self.tipo_espacio = texto_obligatorio(self.tipo_espacio, "tipo_espacio")
        self.actividad_principal = texto_obligatorio(
            self.actividad_principal, "actividad_principal"
        )
        self.direccion = texto_obligatorio(self.direccion, "direccion")
        try:
            aforo = int(self.aforo_aproximado)
        except (TypeError, ValueError) as exc:
            raise ErrorValidacion("El aforo debe ser un número entero") from exc
        if aforo < 0:
            raise ErrorValidacion("El aforo aproximado no puede ser negativo")
        self.aforo_aproximado = aforo

    def propiedades(self) -> dict:
        return {
            "tipo_espacio": self.tipo_espacio,
            "actividad_principal": self.actividad_principal,
            "direccion": self.direccion,
            "aforo_aproximado": self.aforo_aproximado,
        }
