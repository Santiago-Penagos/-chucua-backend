import pytest

from seed.sectores import clasificar_sector, sector_de_coordenadas


@pytest.mark.parametrize(
    "longitud,sector",
    [
        (-74.1705, "I"),
        (-74.1670, "I"),
        (-74.166667, "II"),
        (-74.1650, "II"),
        (-74.162833, "II"),
        (-74.162800, "III"),
        (-74.1590, "III"),
    ],
)
def test_clasificacion_por_tercios(longitud, sector):
    assert clasificar_sector(longitud) == sector


def test_clasificacion_repetible():
    primera = clasificar_sector(-74.164)
    segunda = clasificar_sector(-74.164)
    assert primera == segunda == "II"


def test_sector_de_varios_vertices_usa_longitud_media():
    assert sector_de_coordenadas([(-74.170, 4.62), (-74.169, 4.63)]) == "I"


def test_sin_coordenadas_falla():
    with pytest.raises(ValueError):
        sector_de_coordenadas([])
