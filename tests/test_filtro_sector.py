import pytest

from chucua_backend.repositorios.catastro import RepositorioCatastro
from chucua_backend.repositorios.educativos import RepositorioEducativos
from chucua_backend.repositorios.escenarios import RepositorioEscenarios
from chucua_backend.repositorios.vias import RepositorioVias

from fabrica import catastro, educativo, escenario, via

CASOS = [
    (RepositorioEscenarios, escenario),
    (RepositorioEducativos, educativo),
    (RepositorioVias, via),
    (RepositorioCatastro, catastro),
]


@pytest.mark.parametrize("clase,fabrica", CASOS)
def test_filtrado_por_sector(conexion, clase, fabrica):
    repositorio = clase(conexion)
    repositorio.crear(fabrica(nombre="Uno", sector="I"))
    repositorio.crear(fabrica(nombre="Dos", sector="II"))
    repositorio.crear(fabrica(nombre="Tres", sector="III"))

    assert len(repositorio.listar()) == 3
    assert [e.nombre for e in repositorio.listar("II")] == ["Dos"]
    assert [e.nombre for e in repositorio.listar("III")] == ["Tres"]


@pytest.mark.parametrize("clase,fabrica", CASOS)
def test_sector_sin_coincidencias_devuelve_vacio(conexion, clase, fabrica):
    repositorio = clase(conexion)
    repositorio.crear(fabrica(nombre="Uno", sector="I"))
    assert repositorio.listar("III") == []
