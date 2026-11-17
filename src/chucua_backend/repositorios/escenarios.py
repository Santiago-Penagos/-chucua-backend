from ..dominio.escenario import EscenarioDeportivo
from .base_sqlite import RepositorioSQLiteBase


class RepositorioEscenarios(RepositorioSQLiteBase[EscenarioDeportivo]):
    tabla = "escenarios"
    columnas = ("tipo_escenario",)

    def _valores(self, entidad: EscenarioDeportivo) -> tuple:
        return (entidad.tipo_escenario,)

    def _desde_fila(self, fila) -> EscenarioDeportivo:
        return EscenarioDeportivo(
            nombre=fila["nombre"],
            sector=fila["sector"],
            geometria=self._geometria(fila),
            tipo_escenario=fila["tipo_escenario"],
            osm_id=fila["osm_id"],
            id=fila["id"],
        )
