ESQUEMA = """
CREATE TABLE IF NOT EXISTS escenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osm_id TEXT UNIQUE,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    sector TEXT NOT NULL CHECK (sector IN ('I', 'II', 'III')),
    geometria TEXT NOT NULL CHECK (length(geometria) > 2),
    tipo_escenario TEXT NOT NULL CHECK (length(trim(tipo_escenario)) > 0)
);

CREATE TABLE IF NOT EXISTS educativos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osm_id TEXT UNIQUE,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    sector TEXT NOT NULL CHECK (sector IN ('I', 'II', 'III')),
    geometria TEXT NOT NULL CHECK (length(geometria) > 2),
    nivel_educativo TEXT NOT NULL CHECK (length(trim(nivel_educativo)) > 0),
    naturaleza TEXT NOT NULL CHECK (length(trim(naturaleza)) > 0)
);

CREATE TABLE IF NOT EXISTS vias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osm_id TEXT UNIQUE,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    sector TEXT NOT NULL CHECK (sector IN ('I', 'II', 'III')),
    geometria TEXT NOT NULL CHECK (length(geometria) > 2),
    tipo_via TEXT NOT NULL CHECK (length(trim(tipo_via)) > 0),
    estado TEXT NOT NULL CHECK (length(trim(estado)) > 0)
);

CREATE TABLE IF NOT EXISTS catastro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osm_id TEXT UNIQUE,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    sector TEXT NOT NULL CHECK (sector IN ('I', 'II', 'III')),
    geometria TEXT NOT NULL CHECK (length(geometria) > 2),
    uso_suelo TEXT NOT NULL CHECK (length(trim(uso_suelo)) > 0),
    area_m2 REAL NOT NULL CHECK (area_m2 > 0)
);

CREATE INDEX IF NOT EXISTS idx_escenarios_sector ON escenarios (sector);
CREATE INDEX IF NOT EXISTS idx_educativos_sector ON educativos (sector);
CREATE INDEX IF NOT EXISTS idx_vias_sector ON vias (sector);
CREATE INDEX IF NOT EXISTS idx_catastro_sector ON catastro (sector);
"""


def crear_esquema(conexion) -> None:
    conexion.executescript(ESQUEMA)
    conexion.commit()
