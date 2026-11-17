from ..dominio.via import EstadoVia
from .base_sqlite import RepositorioSQLiteBase


class RepositorioVias(RepositorioSQLiteBase[EstadoVia]):
    tabla = "vias"
    columnas = ("tipo_via", "estado")

    def _valores(self, entidad: EstadoVia) -> tuple:
        return (entidad.tipo_via, entidad.estado)

    def _desde_fila(self, fila) -> EstadoVia:
        return EstadoVia(
            nombre=fila["nombre"],
            sector=fila["sector"],
            geometria=self._geometria(fila),
            tipo_via=fila["tipo_via"],
            estado=fila["estado"],
            osm_id=fila["osm_id"],
            id=fila["id"],
        )
