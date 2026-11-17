from seed.mapeo import mapear_catastro, mapear_educativo, mapear_escenario, mapear_via


def test_escuela_se_convierte_en_centro_educativo():
    elemento = {
        "type": "node",
        "id": 10,
        "lat": 4.628,
        "lon": -74.165,
        "tags": {"name": "Colegio X", "amenity": "school", "operator:type": "public"},
    }
    entidad = mapear_educativo(elemento)
    assert entidad.nombre == "Colegio X"
    assert entidad.nivel_educativo == "basica"
    assert entidad.naturaleza == "publico"
    assert entidad.sector == "II"
    assert entidad.geometria.tipo == "Point"


def test_edificacion_se_convierte_en_catastro():
    elemento = {
        "type": "way",
        "id": 20,
        "geometry": [
            {"lat": 4.625, "lon": -74.169},
            {"lat": 4.625, "lon": -74.1684},
            {"lat": 4.6256, "lon": -74.1684},
            {"lat": 4.6256, "lon": -74.169},
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
            {"lat": 4.627, "lon": -74.162},
            {"lat": 4.6275, "lon": -74.161},
            {"lat": 4.628, "lon": -74.160},
        ],
        "tags": {"highway": "residential"},
    }
    entidad = mapear_via(elemento)
    assert entidad.estado == "sin_evaluar"
    assert entidad.tipo_via == "residential"
    assert entidad.sector == "III"


def test_elemento_sin_nombre_recibe_nombre_descriptivo():
    elemento = {"type": "node", "id": 40, "lat": 4.63, "lon": -74.168, "tags": {}}
    entidad = mapear_escenario(elemento)
    assert "40" in entidad.nombre
    assert entidad.tipo_escenario == "deportivo"
