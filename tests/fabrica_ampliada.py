from chucua_backend.dominio.comercio import ComercioLocal
from chucua_backend.dominio.cultura import EspacioCultural
from chucua_backend.dominio.demografia import DemografiaSector
from chucua_backend.dominio.geometria import Punto
from chucua_backend.dominio.humedal_puntos import PuntoHumedal
from chucua_backend.dominio.jac import JuntaAccionComunal
from chucua_backend.dominio.salud import CentroSalud
from chucua_backend.dominio.seguridad import PuntoSeguridad
from chucua_backend.dominio.servicios_publicos import PuntoServicioPublico
from chucua_backend.dominio.transporte import ParaderoSitp
from chucua_backend.dominio.zonas_verdes import ZonaVerde

PUNTO = Punto((-74.1685, 4.6285))

CLASES = {
    "jac": (JuntaAccionComunal, dict(
        presidente_contacto="Contacto 300 000 0000",
        direccion="Calle 38 Sur # 79-12",
        horario_atencion="Sábados 9:00 a.m.",
    )),
    "centros_salud": (CentroSalud, dict(
        tipo_centro="centro_salud", nivel_atencion="I",
        horario="Lunes a viernes", direccion="Calle 38 Sur # 79-50",
    )),
    "seguridad": (PuntoSeguridad, dict(
        tipo_punto="CAI", cuadrante="Cuadrante 12", telefono_contacto="123",
    )),
    "humedal_puntos": (PuntoHumedal, dict(
        zona_humedal="ronda_norte", estado_conservacion="bueno",
        especie_destacada="Tingua",
    )),
    "transporte": (ParaderoSitp, dict(
        codigo_paradero="SITP-001", rutas_alimentadoras="7-1, 7-2",
        direccion="Calle 38 Sur # 79-30", estado_senalizacion="buena",
    )),
    "comercio": (ComercioLocal, dict(
        categoria_comercial="alimentos", nombre_establecimiento="Panadería La Espiga",
        direccion="Calle 38 Sur # 79-18", horario="Lunes a domingo",
    )),
    "cultura": (EspacioCultural, dict(
        tipo_espacio="casa_cultura", actividad_principal="Talleres de arte",
        direccion="Calle 38 Sur # 79-60", aforo_aproximado=120,
    )),
    "servicios_publicos": (PuntoServicioPublico, dict(
        tipo_servicio="acueducto", estado_operativo="operativo",
        ubicacion_referencia="Junto al humedal",
    )),
    "zonas_verdes": (ZonaVerde, dict(
        area_aprox_m2=3200.0, tipo_vegetacion="arboles_nativos",
        estado_mantenimiento="bueno", direccion="Calle 38 Sur # 79-70",
    )),
    "demografia": (DemografiaSector, dict(
        poblacion_estimada=420, hogares_aprox=120,
        grupo_etario_predominante="adultos", anio_censo=2024,
    )),
}

DOMINIOS = tuple(CLASES)


def ampliada(dominio: str, nombre="Entidad ampliada", sector="I", osm_id=None):
    clase, atributos = CLASES[dominio]
    return clase(
        nombre=nombre,
        sector=sector,
        geometria=PUNTO,
        osm_id=osm_id,
        **atributos,
    )
