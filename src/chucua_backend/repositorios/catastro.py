from ..dominio.catastro import InformacionCatastral
from .base_sqlite import RepositorioSQLiteBase


class RepositorioCatastro(RepositorioSQLiteBase[InformacionCatastral]):
    tabla = "catastro"
    columnas = ("uso_suelo", "area_m2")

    def _valores(self, entidad: InformacionCatastral) -> tuple:
        return (entidad.uso_suelo, entidad.area_m2)

    def _desde_fila(self, fila) -> InformacionCatastral:
        return InformacionCatastral(
            nombre=fila["nombre"],
            sector=fila["sector"],
            geometria=self._geometria(fila),
            uso_suelo=fila["uso_suelo"],
            area_m2=fila["area_m2"],
            osm_id=fila["osm_id"],
            id=fila["id"],
        )
