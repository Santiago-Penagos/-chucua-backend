import pytest

from chucua_backend.repositorios import (
    RepositorioCentrosSalud,
    RepositorioComercio,
    RepositorioCultura,
    RepositorioDemografia,
    RepositorioHumedalPuntos,
    RepositorioJac,
    RepositorioSeguridad,
    RepositorioServiciosPublicos,
    RepositorioTransporte,
    RepositorioZonasVerdes,
)

from fabrica_ampliada import DOMINIOS, ampliada

REPOSITORIOS = {
    "jac": RepositorioJac,
    "centros_salud": RepositorioCentrosSalud,
    "seguridad": RepositorioSeguridad,
    "humedal_puntos": RepositorioHumedalPuntos,
    "transporte": RepositorioTransporte,
    "comercio": RepositorioComercio,
    "cultura": RepositorioCultura,
    "servicios_publicos": RepositorioServiciosPublicos,
    "zonas_verdes": RepositorioZonasVerdes,
    "demografia": RepositorioDemografia,
}


@pytest.mark.parametrize("dominio", DOMINIOS)
def test_ciclo_crud_de_los_diez_dominios(conexion, dominio):
    repositorio = REPOSITORIOS[dominio](conexion)
    creada = repositorio.crear(ampliada(dominio, nombre="Inicial"))
    assert creada.id is not None
    assert repositorio.obtener(creada.id).nombre == "Inicial"

    actualizada = repositorio.actualizar(creada.id, ampliada(dominio, nombre="Nueva"))
    assert actualizada.nombre == "Nueva"
    assert repositorio.listar("I")[0].id == creada.id

    assert repositorio.eliminar(creada.id) is True
    assert repositorio.obtener(creada.id) is None


@pytest.mark.parametrize("dominio", DOMINIOS)
def test_los_atributos_propios_se_conservan(conexion, dominio):
    repositorio = REPOSITORIOS[dominio](conexion)
    original = ampliada(dominio)
    leida = repositorio.obtener(repositorio.crear(original).id)
    assert leida.propiedades() == original.propiedades()


@pytest.mark.parametrize("dominio", DOMINIOS)
def test_upsert_por_osm_id_no_duplica(conexion, dominio):
    repositorio = REPOSITORIOS[dominio](conexion)
    original = repositorio.crear(ampliada(dominio, osm_id=f"respaldo/{dominio}-1"))
    actualizada = repositorio.upsert_por_osm_id(
        ampliada(dominio, nombre="Actualizada", osm_id=f"respaldo/{dominio}-1")
    )
    assert actualizada.id == original.id
    assert len(repositorio.listar()) == 1
