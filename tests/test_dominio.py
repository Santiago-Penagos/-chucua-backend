import pytest

from chucua_backend.dominio.catastro import InformacionCatastral
from chucua_backend.dominio.escenario import EscenarioDeportivo
from chucua_backend.dominio.geometria import Linea, Poligono, Punto
from chucua_backend.errores import ErrorValidacion

from fabrica import catastro, educativo, escenario, via


@pytest.mark.parametrize("sector", ["I", "II", "III"])
def test_sectores_validos(sector):
    assert escenario(sector=sector).get_sector() == sector


@pytest.mark.parametrize("sector", ["IV", "i", "", None])
def test_sectores_invalidos(sector):
    with pytest.raises(ErrorValidacion):
        escenario(sector=sector)


def test_nombre_vacio_rechazado():
    with pytest.raises(ErrorValidacion):
        escenario(nombre="   ")


def test_geometria_incorrecta_por_dominio():
    with pytest.raises(ErrorValidacion):
        EscenarioDeportivo(
            nombre="X",
            sector="I",
            geometria=Linea(((-74.16, 4.62), (-74.159, 4.621))),
            tipo_escenario="cancha",
        )
    with pytest.raises(ErrorValidacion):
        InformacionCatastral(
            nombre="X",
            sector="I",
            geometria=Punto((-74.16, 4.62)),
            uso_suelo="residencial",
            area_m2=10,
        )


def test_area_catastral_no_positiva():
    with pytest.raises(ErrorValidacion):
        InformacionCatastral(
            nombre="X",
            sector="I",
            geometria=Poligono(
                ((-74.169, 4.625), (-74.1684, 4.625), (-74.1684, 4.6256))
            ),
            uso_suelo="residencial",
            area_m2=0,
        )


def test_atributos_propios_en_geojson():
    assert escenario().a_geojson()["properties"]["tipo_escenario"] == "cancha"
    assert educativo().a_geojson()["properties"]["naturaleza"] == "publico"
    assert via().a_geojson()["properties"]["tipo_via"] == "residential"
    assert catastro().a_geojson()["properties"]["area_m2"] == 1200
