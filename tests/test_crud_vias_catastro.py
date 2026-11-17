from chucua_backend.repositorios.catastro import RepositorioCatastro
from chucua_backend.repositorios.vias import RepositorioVias

from fabrica import catastro, via


def test_crud_via_conserva_orden_de_vertices(conexion):
    repositorio = RepositorioVias(conexion)
    creada = repositorio.crear(via(nombre="Carrera 80"))
    leida = repositorio.obtener(creada.id)
    assert leida.nombre == "Carrera 80"
    assert leida.geometria.coordenadas == (
        (-74.162, 4.627),
        (-74.161, 4.6275),
        (-74.16, 4.628),
    )
    assert repositorio.eliminar(creada.id) is True
    assert repositorio.obtener(creada.id) is None


def test_crud_catastro_conserva_area_y_poligono(conexion):
    repositorio = RepositorioCatastro(conexion)
    creada = repositorio.crear(catastro())
    leida = repositorio.obtener(creada.id)
    assert leida.area_m2 == 1200
    assert leida.geometria.a_geojson()["type"] == "Polygon"
    assert leida.geometria.coordenadas[0] == leida.geometria.coordenadas[-1]

    actualizada = repositorio.actualizar(creada.id, catastro(nombre="Predio Nuevo"))
    assert actualizada.nombre == "Predio Nuevo"
    assert actualizada.area_m2 == 1200
