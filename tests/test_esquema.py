import sqlite3

import pytest

from chucua_backend.db.conexion import conectar

GEOMETRIA = '{"type": "Point", "coordinates": [-74.16, 4.62]}'


def test_crea_las_cuatro_tablas(tmp_path):
    base = conectar(tmp_path / "x.db")
    tablas = {
        fila["name"]
        for fila in base.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    assert {"escenarios", "educativos", "vias", "catastro"} <= tablas
    base.close()


def test_inicializacion_repetida_conserva_datos(tmp_path):
    ruta = tmp_path / "x.db"
    base = conectar(ruta)
    base.execute(
        "INSERT INTO escenarios (nombre, sector, geometria, tipo_escenario) VALUES (?,?,?,?)",
        ("Cancha", "I", GEOMETRIA, "cancha"),
    )
    base.commit()
    base.close()
    otra = conectar(ruta)
    total = otra.execute("SELECT COUNT(*) AS n FROM escenarios").fetchone()["n"]
    assert total == 1
    otra.close()


def test_sector_invalido_rechazado_por_la_base(conexion):
    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute(
            "INSERT INTO escenarios (nombre, sector, geometria, tipo_escenario) VALUES (?,?,?,?)",
            ("Cancha", "IV", GEOMETRIA, "cancha"),
        )


def test_registro_sin_nombre_o_geometria_rechazado(conexion):
    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute(
            "INSERT INTO escenarios (nombre, sector, geometria, tipo_escenario) VALUES (?,?,?,?)",
            (None, "I", GEOMETRIA, "cancha"),
        )
    with pytest.raises(sqlite3.IntegrityError):
        conexion.execute(
            "INSERT INTO escenarios (nombre, sector, geometria, tipo_escenario) VALUES (?,?,?,?)",
            ("Cancha", "I", None, "cancha"),
        )
