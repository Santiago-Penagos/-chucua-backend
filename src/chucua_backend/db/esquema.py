COMUNES = (
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "osm_id TEXT UNIQUE",
    "nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0)",
    "sector TEXT NOT NULL CHECK (sector IN ('I', 'II', 'III'))",
    "geometria TEXT NOT NULL CHECK (length(geometria) > 2)",
)


def texto(campo: str) -> str:
    return f"{campo} TEXT NOT NULL CHECK (length(trim({campo})) > 0)"


def real(campo: str) -> str:
    return f"{campo} REAL NOT NULL CHECK ({campo} > 0)"


def entero(campo: str, minimo: int = 0, maximo: int | None = None) -> str:
    limite = f" AND {campo} <= {maximo}" if maximo is not None else ""
    return f"{campo} INTEGER NOT NULL CHECK ({campo} >= {minimo}{limite})"


COLUMNAS = {
    "escenarios": (texto("tipo_escenario"),),
    "educativos": (texto("nivel_educativo"), texto("naturaleza")),
    "vias": (texto("tipo_via"), texto("estado")),
    "catastro": (texto("uso_suelo"), real("area_m2")),
    "jac": (texto("presidente_contacto"), texto("direccion"), texto("horario_atencion")),
    "centros_salud": (
        texto("tipo_centro"), texto("nivel_atencion"),
        texto("horario"), texto("direccion"),
    ),
    "seguridad": (texto("tipo_punto"), texto("cuadrante"), texto("telefono_contacto")),
    "humedal_puntos": (
        texto("zona_humedal"), texto("estado_conservacion"),
        texto("especie_destacada"),
    ),
    "transporte": (
        texto("codigo_paradero"), texto("rutas_alimentadoras"),
        texto("direccion"), texto("estado_senalizacion"),
    ),
    "comercio": (
        texto("categoria_comercial"), texto("nombre_establecimiento"),
        texto("direccion"), texto("horario"),
    ),
    "cultura": (
        texto("tipo_espacio"), texto("actividad_principal"),
        texto("direccion"), entero("aforo_aproximado"),
    ),
    "servicios_publicos": (
        texto("tipo_servicio"), texto("estado_operativo"),
        texto("ubicacion_referencia"),
    ),
    "zonas_verdes": (
        real("area_aprox_m2"), texto("tipo_vegetacion"),
        texto("estado_mantenimiento"), texto("direccion"),
    ),
    "demografia": (
        entero("poblacion_estimada"), entero("hogares_aprox"),
        texto("grupo_etario_predominante"),
        entero("anio_censo", minimo=1900, maximo=2100),
    ),
}


def definicion_tabla(nombre: str, propias: tuple[str, ...]) -> str:
    columnas = ",\n    ".join(COMUNES + propias)
    return (
        f"CREATE TABLE IF NOT EXISTS {nombre} (\n    {columnas}\n);\n"
        f"CREATE INDEX IF NOT EXISTS idx_{nombre}_sector ON {nombre} (sector);"
    )


ESQUEMA = "\n\n".join(
    definicion_tabla(nombre, propias) for nombre, propias in COLUMNAS.items()
)


def crear_esquema(conexion) -> None:
    conexion.executescript(ESQUEMA)
    conexion.commit()
