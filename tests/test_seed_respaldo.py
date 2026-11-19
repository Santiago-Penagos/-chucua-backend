from seed.constructores import DOMINIOS
from seed.respaldo import cargar_dominio, cargar_todo

TIPOS = {
    "escenarios": "Point",
    "educativos": "Point",
    "vias": "LineString",
    "catastro": "Polygon",
    "jac": "Point",
    "centros_salud": "Point",
    "seguridad": "Point",
    "humedal_puntos": "Point",
    "transporte": "Point",
    "comercio": "Point",
    "cultura": "Point",
    "servicios_publicos": "Point",
    "zonas_verdes": "Point",
    "demografia": "Point",
}


TAMANOS = {"escenarios": 5, "educativos": 3, "jac": 8}
SECTORES = {"escenarios": {"I"}, "educativos": {"I", "II"}, "jac": {"I", "II", "III"}}


def test_respaldo_cubre_los_catorce_dominios():
    datos = cargar_todo()
    assert set(datos) == set(DOMINIOS) == set(TIPOS)
    for dominio, entidades in datos.items():
        assert len(entidades) >= TAMANOS.get(dominio, 3)
        esperados = SECTORES.get(dominio, {"I", "II", "III"})
        assert {e.sector for e in entidades} == esperados


def test_respaldo_tiene_geometrias_y_atributos_validos():
    for dominio, tipo in TIPOS.items():
        for entidad in cargar_dominio(dominio):
            assert entidad.nombre
            assert entidad.geometria.a_geojson()["type"] == tipo
            assert entidad.osm_id.startswith(("respaldo/", "ideca/", "idpac/"))


def test_respaldo_de_catastro_tiene_area_positiva():
    for entidad in cargar_dominio("catastro"):
        assert entidad.area_m2 > 0
