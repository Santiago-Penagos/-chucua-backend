import pytest

from chucua_backend.dominio.geometria import Punto
from chucua_backend.dominio.zonas_verdes import ZonaVerde
from chucua_backend.errores import ErrorValidacion

from fabrica_ampliada import ampliada

PUNTO = Punto((-74.1685, 4.6285))


def test_zona_verde_exige_punto_y_area_positiva():
    with pytest.raises(ErrorValidacion):
        ZonaVerde(
            nombre="X",
            sector="I",
            geometria=PUNTO,
            area_aprox_m2=0,
            tipo_vegetacion="mixta",
            estado_mantenimiento="bueno",
            direccion="Calle 1",
        )
    with pytest.raises(ErrorValidacion):
        ZonaVerde(
            nombre="X",
            sector="I",
            geometria=PUNTO,
            area_aprox_m2=100,
            tipo_vegetacion="  ",
            estado_mantenimiento="bueno",
            direccion="Calle 1",
        )


def test_demografia_rechaza_anio_fuera_de_rango():
    with pytest.raises(ErrorValidacion):
        ampliada("demografia").__class__(
            nombre="X",
            sector="I",
            geometria=PUNTO,
            poblacion_estimada=10,
            hogares_aprox=3,
            grupo_etario_predominante="mixto",
            anio_censo=1800,
        )


def test_jac_y_transporte_publican_sus_atributos():
    assert ampliada("jac").a_geojson()["properties"]["direccion"]
    assert ampliada("transporte").a_geojson()["properties"]["codigo_paradero"]
