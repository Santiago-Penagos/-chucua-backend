import json
import sqlite3
from typing import Generic

from ..dominio.geometria_parser import desde_geojson
from ..dominio.sector import validar_sector
from ..errores import EntidadNoEncontrada, ErrorValidacion
from .contrato import IRepositorioCRUD, T


class RepositorioSQLiteBase(IRepositorioCRUD[T], Generic[T]):
    """Implementa el CRUD común; las subclases declaran tabla y columnas."""

    tabla: str = ""
    columnas: tuple[str, ...] = ()

    def __init__(self, conexion: sqlite3.Connection):
        self._db = conexion

    def _valores(self, entidad: T) -> tuple:
        raise NotImplementedError

    def _desde_fila(self, fila: sqlite3.Row) -> T:
        raise NotImplementedError

    def _geometria(self, fila: sqlite3.Row):
        return desde_geojson(json.loads(fila["geometria"]))

    def _parametros(self, entidad) -> tuple:
        geometria = json.dumps(entidad.geometria.a_geojson(), ensure_ascii=False)
        return (entidad.osm_id, entidad.nombre, entidad.sector, geometria, *self._valores(entidad))

    def _columnas_sql(self) -> str:
        propias = ", ".join(self.columnas)
        return f"osm_id, nombre, sector, geometria, {propias}"

    def _marcadores(self) -> str:
        return ", ".join("?" for _ in range(4 + len(self.columnas)))

    def _fila(self, entidad_id: int):
        return self._db.execute(
            f"SELECT * FROM {self.tabla} WHERE id = ?", (entidad_id,)
        ).fetchone()

    def crear(self, entidad: T) -> T:
        sql = f"INSERT INTO {self.tabla} ({self._columnas_sql()}) VALUES ({self._marcadores()})"
        try:
            cursor = self._db.execute(sql, self._parametros(entidad))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ErrorValidacion(f"No se pudo guardar en {self.tabla}: {exc}") from exc
        return self.obtener(cursor.lastrowid)

    def obtener(self, entidad_id: int) -> T | None:
        fila = self._fila(entidad_id)
        return self._desde_fila(fila) if fila else None

    def listar(self, sector: str | None = None) -> list[T]:
        if sector is not None:
            validar_sector(sector)
        sql = f"SELECT * FROM {self.tabla}"
        parametros: tuple = ()
        if sector is not None:
            sql += " WHERE sector = ?"
            parametros = (sector,)
        filas = self._db.execute(sql + " ORDER BY id", parametros).fetchall()
        return [self._desde_fila(fila) for fila in filas]

    def actualizar(self, entidad_id: int, entidad: T) -> T:
        asignaciones = ", ".join(f"{c} = ?" for c in ("osm_id", "nombre", "sector", "geometria", *self.columnas))
        sql = f"UPDATE {self.tabla} SET {asignaciones} WHERE id = ?"
        try:
            cursor = self._db.execute(sql, (*self._parametros(entidad), entidad_id))
            self._db.commit()
        except sqlite3.IntegrityError as exc:
            raise ErrorValidacion(f"No se pudo actualizar en {self.tabla}: {exc}") from exc
        if cursor.rowcount == 0:
            raise EntidadNoEncontrada(f"{self.tabla} con id {entidad_id} no existe")
        return self.obtener(entidad_id)

    def eliminar(self, entidad_id: int) -> bool:
        cursor = self._db.execute(f"DELETE FROM {self.tabla} WHERE id = ?", (entidad_id,))
        self._db.commit()
        if cursor.rowcount == 0:
            raise EntidadNoEncontrada(f"{self.tabla} con id {entidad_id} no existe")
        return True

    def upsert_por_osm_id(self, entidad: T) -> T:
        if not entidad.osm_id:
            return self.crear(entidad)
        fila = self._db.execute(
            f"SELECT id FROM {self.tabla} WHERE osm_id = ?", (entidad.osm_id,)
        ).fetchone()
        return self.actualizar(fila["id"], entidad) if fila else self.crear(entidad)
