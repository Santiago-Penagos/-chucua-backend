from collections import Counter

from chucua_backend.geografia import (
    LIMITES_BARRIO,
    SECTORES,
    anillo_sector,
    contiene_punto,
)

from seed.constructores import DOMINIOS
from seed.respaldo import cargar_dominio

DOMINIOS_PUNTUALES = (
    "jac",
    "centros_salud",
    "seguridad",
    "humedal_puntos",
    "transporte",
    "comercio",
    "cultura",
    "servicios_publicos",
    "zonas_verdes",
    "demografia",
)


def _area_grados(anillo) -> float:
    suma = sum(
        x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(anillo, anillo[1:])
    )
    return abs(suma) / 2


def test_sectores_oficiales_ideca_son_poligonos_cerrados():
    assert LIMITES_BARRIO["sur"] < LIMITES_BARRIO["norte"]
    assert LIMITES_BARRIO["occidente"] < LIMITES_BARRIO["oriente"]
    for sector in SECTORES:
        anillo = anillo_sector(sector)
        assert anillo[0] == anillo[-1]
        assert _area_grados(anillo) > 0


def test_registros_de_los_catorce_dominios_caen_en_su_sector():
    for dominio in DOMINIOS:
        conteo = Counter()
        for entidad in cargar_dominio(dominio):
            for longitud, latitud in entidad.get_coordenadas():
                assert contiene_punto(entidad.sector, longitud, latitud)
            conteo[entidad.sector] += 1
        if dominio == "escenarios":
            assert conteo == Counter({"I": 5})
        elif dominio == "educativos":
            assert conteo == Counter({"I": 2, "II": 1})
        elif dominio == "salud":
            assert conteo == Counter()
        elif dominio == "jac":
            assert conteo == Counter({"I": 4, "II": 2, "III": 2})
        else:
            assert conteo == Counter({"I": 2, "II": 2, "III": 2})


def test_diez_dominios_puntuales_tienen_sesenta_y_dos_coordenadas_unicas():
    coordenadas = []
    for dominio in DOMINIOS_PUNTUALES:
        for entidad in cargar_dominio(dominio):
            coordenadas.append(tuple(entidad.geometria.coordenada))
    assert len(coordenadas) == len(set(coordenadas)) == 62


def test_nombres_sin_identificadores_crudos_de_osm():
    for dominio in DOMINIOS:
        for entidad in cargar_dominio(dominio):
            assert "way/" not in entidad.nombre
            assert "node/" not in entidad.nombre
