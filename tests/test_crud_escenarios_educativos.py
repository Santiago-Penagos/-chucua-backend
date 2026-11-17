import pytest

from chucua_backend.repositorios.educativos import RepositorioEducativos
from chucua_backend.repositorios.escenarios import RepositorioEscenarios

from fabrica import educativo, escenario


@pytest.mark.parametrize(
    "clase,fabrica",
    [(RepositorioEscenarios, escenario), (RepositorioEducativos, educativo)],
)
def test_ciclo_crud_completo(conexion, clase, fabrica):
    repositorio = clase(conexion)
    creada = repositorio.crear(fabrica(nombre="Inicial"))
    assert creada.id is not None
    assert repositorio.obtener(creada.id).nombre == "Inicial"

    actualizada = repositorio.actualizar(creada.id, fabrica(nombre="Actualizada"))
    assert actualizada.id == creada.id
    assert actualizada.nombre == "Actualizada"

    assert repositorio.eliminar(creada.id) is True
    assert repositorio.obtener(creada.id) is None


def test_conserva_atributos_y_geometria(conexion):
    repositorio = RepositorioEscenarios(conexion)
    creada = repositorio.crear(escenario(tipo_escenario="gimnasio"))
    leida = repositorio.obtener(creada.id)
    assert leida.tipo_escenario == "gimnasio"
    assert leida.geometria.a_geojson() == {
        "type": "Point",
        "coordinates": [-74.1685, 4.6285],
    }
