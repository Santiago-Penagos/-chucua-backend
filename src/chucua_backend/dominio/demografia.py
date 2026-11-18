from ..errores import ErrorValidacion
from .entidad import EntidadGeografica, texto_obligatorio
from .geometria import Punto


class DemografiaSector(EntidadGeografica):
    """Indicador demográfico agregado por manzana o sector."""

    def __init__(
        self,
        *,
        nombre,
        sector,
        geometria,
        poblacion_estimada,
        hogares_aprox,
        grupo_etario_predominante,
        anio_censo,
        osm_id=None,
        id=None,
    ):
        self.poblacion_estimada = poblacion_estimada
        self.hogares_aprox = hogares_aprox
        self.grupo_etario_predominante = grupo_etario_predominante
        self.anio_censo = anio_censo
        super().__init__(
            nombre=nombre, sector=sector, geometria=geometria, osm_id=osm_id, id=id
        )

    def validar(self) -> None:
        if not isinstance(self.geometria, Punto):
            raise ErrorValidacion("Un registro demográfico debe ser un punto")
        self.poblacion_estimada = _entero(
            self.poblacion_estimada, "poblacion_estimada", minimo=0
        )
        self.hogares_aprox = _entero(self.hogares_aprox, "hogares_aprox", minimo=0)
        self.anio_censo = _entero(self.anio_censo, "anio_censo", minimo=1900, maximo=2100)
        self.grupo_etario_predominante = texto_obligatorio(
            self.grupo_etario_predominante, "grupo_etario_predominante"
        )

    def propiedades(self) -> dict:
        return {
            "poblacion_estimada": self.poblacion_estimada,
            "hogares_aprox": self.hogares_aprox,
            "grupo_etario_predominante": self.grupo_etario_predominante,
            "anio_censo": self.anio_censo,
        }


def _entero(valor, campo: str, *, minimo: int, maximo: int | None = None) -> int:
    try:
        numero = int(valor)
    except (TypeError, ValueError) as exc:
        raise ErrorValidacion(f"El campo '{campo}' debe ser un número entero") from exc
    if numero < minimo or (maximo is not None and numero > maximo):
        raise ErrorValidacion(f"El campo '{campo}' está fuera de rango")
    return numero
