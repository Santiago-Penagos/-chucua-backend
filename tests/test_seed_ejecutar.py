from seed.ejecutar import sembrar


def test_semilla_de_respaldo_carga_los_cuatro_dominios(conexion):
    reporte = sembrar("respaldo", conexion=conexion, usar_red=False)
    assert reporte["fuente"] == "respaldo"
    assert reporte["total"] == 24
    assert reporte["dominios"] == {
        "escenarios": 6,
        "educativos": 6,
        "vias": 6,
        "catastro": 6,
    }
    assert reporte["sectores"] == {"I": 8, "II": 8, "III": 8}


def test_semilla_es_idempotente(conexion):
    primera = sembrar("respaldo", conexion=conexion, usar_red=False)
    segunda = sembrar("respaldo", conexion=conexion, usar_red=False)
    assert primera["total"] == segunda["total"]
    assert primera["dominios"] == segunda["dominios"]


def test_fuente_auto_sin_red_usa_respaldo(conexion):
    reporte = sembrar("auto", conexion=conexion, usar_red=False)
    assert reporte["fuente"] == "respaldo"
    assert all(valor == "respaldo" for valor in reporte["detalle_fuente"].values())
