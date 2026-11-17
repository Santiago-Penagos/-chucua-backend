from seed.overpass import BBOX, construir_consulta, consultar, consultar_todo


def test_consulta_contiene_el_bounding_box():
    consulta = construir_consulta("escenarios")
    for valor in BBOX:
        assert str(valor) in consulta
    assert "leisure" in consulta


def test_consulta_de_vias_filtra_highway():
    consulta = construir_consulta("vias")
    assert "highway" in consulta
    assert "residential" in consulta


def test_consulta_exitosa_devuelve_elementos():
    def obtener(consulta, timeout):
        return {"elements": [{"type": "node", "id": 1}]}

    assert consultar("vias", obtener=obtener, dormir=lambda _: None) == [
        {"type": "node", "id": 1}
    ]


def test_timeout_agotado_no_propaga_error():
    llamadas = []

    def obtener(consulta, timeout):
        llamadas.append(consulta)
        raise TimeoutError("sin red")

    resultado = consultar(
        "escenarios", reintentos=2, obtener=obtener, dormir=lambda _: None
    )
    assert resultado == []
    assert len(llamadas) == 3


def test_consultar_todo_devuelve_cuatro_dominios():
    def obtener(consulta, timeout):
        return {"elements": []}

    resultado = consultar_todo(obtener=obtener, dormir=lambda _: None)
    assert set(resultado) == {"escenarios", "educativos", "vias", "catastro"}
