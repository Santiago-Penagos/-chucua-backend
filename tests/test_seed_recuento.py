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
POR_DOMINIO = 6
TOTAL = len(DOMINIOS) * POR_DOMINIO
POR_SECTOR = TOTAL // 3


def test_semilla_de_respaldo_carga_los_catorce_dominios(conexion):
    from seed.ejecutar import sembrar

    reporte = sembrar("respaldo", conexion=conexion, usar_red=False)
    assert reporte["fuente"] == "respaldo"
    assert reporte["total"] == TOTAL
    assert reporte["dominios"] == {dominio: POR_DOMINIO for dominio in DOMINIOS}
    assert reporte["sectores"] == {"I": POR_SECTOR, "II": POR_SECTOR, "III": POR_SECTOR}
