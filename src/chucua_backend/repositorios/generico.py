from .base_sqlite import RepositorioSQLiteBase


class RepositorioGenerico(RepositorioSQLiteBase):
    """Repositorio CRUD configurable por tabla, columnas y clase de dominio."""

    def __init__(self, conexion, *, tabla: str, columnas: tuple, entidad):
        self._db = conexion
        self.tabla = tabla
        self.columnas = tuple(columnas)
        self._entidad = entidad

    def _valores(self, entidad) -> tuple:
        return tuple(getattr(entidad, columna) for columna in self.columnas)

    def _desde_fila(self, fila):
        return self._entidad(
            nombre=fila["nombre"],
            sector=fila["sector"],
            geometria=self._geometria(fila),
            osm_id=fila["osm_id"],
            id=fila["id"],
            **{columna: fila[columna] for columna in self.columnas},
        )
