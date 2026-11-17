import pytest

from chucua_backend.dominio.geometria import Linea, Poligono, Punto
from chucua_backend.errores import ErrorValidacion


def test_punto_serializa_longitud_latitud():
    punto = Punto((-74.1685, 4.6285))
    assert punto.a_geojson() == {"type": "Point", "coordinates": [-74.1685, 4.6285]}


def test_coordenada_fuera_de_rango_falla():
    with pytest.raises(ErrorValidacion):
        Punto((200, 4.62))
    with pytest.raises(ErrorValidacion):
        Punto((-74.16, 95))


def test_linea_requiere_dos_vertices():
    with pytest.raises(ErrorValidacion):
        Linea(((-74.16, 4.62),))
    linea = Linea(((-74.16, 4.62), (-74.159, 4.621)))
    assert linea.a_geojson()["type"] == "LineString"


def test_poligono_cierra_el_anillo():
    poligono = Poligono(((-74.16, 4.62), (-74.159, 4.62), (-74.159, 4.621)))
    assert poligono.coordenadas[0] == poligono.coordenadas[-1]
    assert len(poligono.coordenadas) == 4
    assert poligono.a_geojson()["coordinates"][0][0] == [-74.16, 4.62]


def test_poligono_requiere_tres_vertices_distintos():
    with pytest.raises(ErrorValidacion):
        Poligono(((-74.16, 4.62), (-74.159, 4.62), (-74.16, 4.62)))


def test_area_del_poligono_es_positiva():
    poligono = Poligono(
        ((-74.169, 4.625), (-74.1684, 4.625), (-74.1684, 4.6256), (-74.169, 4.6256))
    )
    assert poligono.area_m2() > 0
