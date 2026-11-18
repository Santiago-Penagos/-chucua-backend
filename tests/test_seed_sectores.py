import json

import pytest

from chucua_backend.errores import ErrorValidacion
from chucua_backend.geografia import coleccion_sectores

from seed.respaldo import RUTA_DATOS
from seed.sectores import clasificar_sector, sector_de_coordenadas


@pytest.mark.parametrize(
    "longitud,latitud,sector",
    [
        (-74.1680, 4.6305, "I"),
        (-74.1650, 4.6309, "I"),
        (-74.1640, 4.6295, "I"),
        (-74.1670, 4.6280, "II"),
        (-74.1640, 4.6270, "II"),
        (-74.1632, 4.6285, "II"),
        (-74.1680, 4.6250, "III"),
        (-74.1650, 4.6245, "III"),
        (-74.1625, 4.6260, "III"),
    ],
)
def test_clasificacion_dentro_de_los_poligonos(longitud, latitud, sector):
    assert clasificar_sector(longitud, latitud) == sector


def test_clasificacion_repetible():
    primera = clasificar_sector(-74.1650, 4.6280)
    segunda = clasificar_sector(-74.1650, 4.6280)
    assert primera == segunda == "II"


def test_punto_fuera_del_barrio_falla():
    with pytest.raises(ErrorValidacion):
        clasificar_sector(-74.1700, 4.6280)
    with pytest.raises(ErrorValidacion):
        clasificar_sector(-74.1600, 4.6300)


def test_sector_de_varios_vertices_usa_el_promedio():
    assert sector_de_coordenadas([(-74.1680, 4.6302), (-74.1684, 4.6306)]) == "I"


def test_geometria_que_sale_del_barrio_falla():
    with pytest.raises(ErrorValidacion):
        sector_de_coordenadas([(-74.1680, 4.6302), (-74.1700, 4.6280)])


def test_sin_coordenadas_falla():
    with pytest.raises(ValueError):
        sector_de_coordenadas([])


def test_geojson_de_sectores_coincide_con_los_poligonos():
    datos = json.loads(
        (RUTA_DATOS / "sectores_barrio.geojson").read_text(encoding="utf-8")
    )
    assert datos == coleccion_sectores()
    assert {f["properties"]["sector"] for f in datos["features"]} == {"I", "II", "III"}
