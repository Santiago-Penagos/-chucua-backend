import json

import pytest

from chucua_backend.errores import ErrorValidacion
from chucua_backend.geografia import coleccion_sectores

from seed.respaldo import RUTA_DATOS
from seed.sectores import clasificar_sector, sector_de_coordenadas


@pytest.mark.parametrize(
    "longitud,latitud,sector",
    [
        (-74.16888, 4.625369, "I"),
        (-74.16888, 4.628314, "I"),
        (-74.167893, 4.622424, "I"),
        (-74.167474, 4.628764, "II"),
        (-74.167474, 4.630072, "II"),
        (-74.16621, 4.627455, "II"),
        (-74.166064, 4.631183, "III"),
        (-74.164995, 4.630162, "III"),
        (-74.164995, 4.631183, "III"),
    ],
)
def test_clasificacion_dentro_de_los_poligonos(longitud, latitud, sector):
    assert clasificar_sector(longitud, latitud) == sector


def test_clasificacion_repetible():
    primera = clasificar_sector(-74.167474, 4.628764)
    segunda = clasificar_sector(-74.167474, 4.628764)
    assert primera == segunda == "II"


def test_punto_fuera_del_barrio_falla():
    with pytest.raises(ErrorValidacion):
        clasificar_sector(-74.1750, 4.6280)
    with pytest.raises(ErrorValidacion):
        clasificar_sector(-74.1550, 4.6300)


def test_sector_de_varios_vertices_usa_el_promedio():
    assert sector_de_coordenadas([(-74.167827, 4.623995), (-74.167777, 4.624045)]) == "I"


def test_geometria_que_sale_del_barrio_falla():
    with pytest.raises(ErrorValidacion):
        sector_de_coordenadas([(-74.16888, 4.625369), (-74.1750, 4.6280)])


def test_sin_coordenadas_falla():
    with pytest.raises(ValueError):
        sector_de_coordenadas([])


def test_geojson_de_sectores_coincide_con_los_poligonos():
    datos = json.loads(
        (RUTA_DATOS / "sectores_barrio.geojson").read_text(encoding="utf-8")
    )
    assert datos == coleccion_sectores()
    assert {f["properties"]["sector"] for f in datos["features"]} == {"I", "II", "III"}
