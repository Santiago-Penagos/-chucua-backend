from ..dominio.educativo import CentroEducativo
from .base_sqlite import RepositorioSQLiteBase


class RepositorioEducativos(RepositorioSQLiteBase[CentroEducativo]):
    tabla = "educativos"
    columnas = ("nivel_educativo", "naturaleza")

    def _valores(self, entidad: CentroEducativo) -> tuple:
        return (entidad.nivel_educativo, entidad.naturaleza)

    def _desde_fila(self, fila) -> CentroEducativo:
        return CentroEducativo(
            nombre=fila["nombre"],
            sector=fila["sector"],
            geometria=self._geometria(fila),
            nivel_educativo=fila["nivel_educativo"],
            naturaleza=fila["naturaleza"],
            osm_id=fila["osm_id"],
            id=fila["id"],
        )
