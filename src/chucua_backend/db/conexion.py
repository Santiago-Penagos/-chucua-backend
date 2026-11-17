import os
import sqlite3
from pathlib import Path

# chucua-backend/chucua.db por defecto, independiente del directorio de trabajo.
RUTA_PREDETERMINADA = Path(__file__).resolve().parents[3] / "chucua.db"


def ruta_bd() -> str:
    return os.environ.get("CHUCUA_DB_PATH") or str(RUTA_PREDETERMINADA)


def _cargar_spatialite(conexion: sqlite3.Connection) -> bool:
    try:
        conexion.enable_load_extension(True)
        conexion.load_extension("mod_spatialite")
        conexion.enable_load_extension(False)
        return True
    except (AttributeError, sqlite3.OperationalError):
        return False


def conectar(ruta: str | Path | None = None) -> sqlite3.Connection:
    destino = str(ruta or ruta_bd())
    if destino != ":memory:":
        Path(destino).parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(destino, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.execute("PRAGMA busy_timeout = 5000")
    _cargar_spatialite(conexion)
    from .esquema import crear_esquema

    crear_esquema(conexion)
    return conexion
