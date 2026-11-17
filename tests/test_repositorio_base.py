from chucua_backend.repositorios.contrato import IRepositorioCRUD
from chucua_backend.repositorios.escenarios import RepositorioEscenarios

from fabrica import escenario


def test_repositorio_cumple_el_contrato():
    assert isinstance(RepositorioEscenarios(None), IRepositorioCRUD)


def test_upsert_actualiza_en_lugar_de_duplicar(conexion):
    repositorio = RepositorioEscenarios(conexion)
    original = repositorio.crear(escenario(nombre="Original", osm_id="node/1"))
    actualizada = repositorio.upsert_por_osm_id(
        escenario(nombre="Actualizada", osm_id="node/1")
    )
    assert actualizada.id == original.id
    assert actualizada.nombre == "Actualizada"
    assert len(repositorio.listar()) == 1


def test_sql_parametrico_evita_inyeccion(conexion):
    repositorio = RepositorioEscenarios(conexion)
    nombre = "x'); DROP TABLE escenarios; --"
    repositorio.crear(escenario(nombre=nombre))
    assert repositorio.obtener(1).nombre == nombre
