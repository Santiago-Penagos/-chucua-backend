import sys
from pathlib import Path

import pytest

RAIZ_BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_BACKEND))

from chucua_backend.db.conexion import conectar  # noqa: E402


@pytest.fixture()
def conexion(tmp_path):
    base = conectar(tmp_path / "prueba.db")
    yield base
    base.close()
