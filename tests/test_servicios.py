import pytest

from chucua_backend.errores import EntidadNoEncontrada
from chucua_backend.servicios.escenarios import ServicioEscenarios


class RepositorioDoble:
    def __init__(self):
        self.llamadas = []
        self.entidad = object()

    def crear(self, entidad):
        self.llamadas.append(("crear", entidad))
        return entidad

    def obtener(self, entidad_id):
        self.llamadas.append(("obtener", entidad_id))
        return self.entidad if entidad_id == 1 else None

    def listar(self, sector=None):
        self.llamadas.append(("listar", sector))
        return [self.entidad]

    def actualizar(self, entidad_id, entidad):
        self.llamadas.append(("actualizar", entidad_id, entidad))
        return entidad

    def eliminar(self, entidad_id):
        self.llamadas.append(("eliminar", entidad_id))
        return True

    def upsert_por_osm_id(self, entidad):
        return entidad


def test_servicio_depende_solo_del_contrato():
    doble = RepositorioDoble()
    servicio = ServicioEscenarios(doble)
    servicio.crear("nueva")
    servicio.obtener(1)
    servicio.listar("II")
    servicio.actualizar(1, "cambiada")
    servicio.eliminar(1)
    assert [llamada[0] for llamada in doble.llamadas] == [
        "crear",
        "obtener",
        "listar",
        "actualizar",
        "eliminar",
    ]


def test_obtener_inexistente_lanza_error():
    servicio = ServicioEscenarios(RepositorioDoble())
    with pytest.raises(EntidadNoEncontrada):
        servicio.obtener(99)
