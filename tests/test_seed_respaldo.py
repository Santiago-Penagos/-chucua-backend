from seed.respaldo import cargar_dominio, cargar_todo

TIPOS = {
    "escenarios": "Point",
    "educativos": "Point",
    "vias": "LineString",
    "catastro": "Polygon",
}


def test_respaldo_cubre_los_cuatro_dominios():
    datos = cargar_todo()
    assert set(datos) == set(TIPOS)
    for dominio, entidades in datos.items():
        assert len(entidades) >= 3
        assert {e.sector for e in entidades} == {"I", "II", "III"}


def test_respaldo_tiene_geometrias_y_atributos_validos():
    for dominio, tipo in TIPOS.items():
        for entidad in cargar_dominio(dominio):
            assert entidad.nombre
            assert entidad.geometria.a_geojson()["type"] == tipo
            assert entidad.osm_id.startswith("respaldo/")


def test_respaldo_de_catastro_tiene_area_positiva():
    for entidad in cargar_dominio("catastro"):
        assert entidad.area_m2 > 0
