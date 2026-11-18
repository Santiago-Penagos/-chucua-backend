from seed.mapeo import mapear_catastro, mapear_educativo, mapear_escenario, mapear_via


def test_escuela_se_convierte_en_centro_educativo():
    elemento = {
        "type": "node",
        "id": 10,
        "lat": 4.6305,
        "lon": -74.1680,
        "tags": {"name": "Colegio X", "amenity": "school", "operator:type": "public"},
    }
    entidad = mapear_educativo(elemento)
    assert entidad.nombre == "Colegio X"
    assert entidad.nivel_educativo == "basica"
    assert entidad.naturaleza == "publico"
    assert entidad.sector == "I"
    assert entidad.geometria.tipo == "Point"


def test_edificacion_se_convierte_en_catastro():
    elemento = {
        "type": "way",
        "id": 20,
        "geometry": [
            {"lat": 4.6302, "lon": -74.1687},
            {"lat": 4.6302, "lon": -74.1681},
            {"lat": 4.6307, "lon": -74.1681},
            {"lat": 4.6307, "lon": -74.1687},
        ],
        "tags": {"building": "yes"},
    }
    entidad = mapear_catastro(elemento)
    assert entidad.uso_suelo == "residencial"
    assert entidad.area_m2 > 0
    assert entidad.sector == "I"
    assert entidad.geometria.tipo == "Polygon"


def test_via_sin_estado_usa_sin_evaluar():
    elemento = {
        "type": "way",
        "id": 30,
        "geometry": [
            {"lat": 4.6270, "lon": -74.1660},
            {"lat": 4.6272, "lon": -74.1655},
            {"lat": 4.6274, "lon": -74.1650},
        ],
        "tags": {"highway": "residential"},
    }
    entidad = mapear_via(elemento)
    assert entidad.estado == "sin_evaluar"
    assert entidad.tipo_via == "residential"
    assert entidad.sector == "II"


def test_elemento_sin_nombre_recibe_nombre_descriptivo():
    elemento = {"type": "node", "id": 40, "lat": 4.6308, "lon": -74.1685, "tags": {}}
    entidad = mapear_escenario(elemento)
    assert "40" in entidad.nombre
    assert "way/" not in entidad.nombre
    assert entidad.tipo_escenario == "deportivo"
