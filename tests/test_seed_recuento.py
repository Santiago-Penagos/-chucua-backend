DOMINIOS = (
    "escenarios",
    "educativos",
    "vias",
    "catastro",
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
POR_DOMINIO = {dominio: 6 for dominio in DOMINIOS}
POR_DOMINIO["escenarios"] = 5
POR_DOMINIO["educativos"] = 3
POR_DOMINIO["jac"] = 8
TOTAL = sum(POR_DOMINIO.values())
POR_SECTOR = {"I": 29, "II": 22, "III": 20}


def test_semilla_de_respaldo_carga_los_catorce_dominios(conexion):
    from seed.ejecutar import sembrar

    reporte = sembrar("respaldo", conexion=conexion, usar_red=False)
    assert reporte["fuente"] == "respaldo"
    assert reporte["total"] == TOTAL
    assert reporte["dominios"] == POR_DOMINIO
    assert reporte["sectores"] == POR_SECTOR


