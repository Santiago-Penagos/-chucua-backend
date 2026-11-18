from chucua_backend.dominio.catastro import InformacionCatastral
from chucua_backend.dominio.comercio import ComercioLocal
from chucua_backend.dominio.cultura import EspacioCultural
from chucua_backend.dominio.demografia import DemografiaSector
from chucua_backend.dominio.educativo import CentroEducativo
from chucua_backend.dominio.escenario import EscenarioDeportivo
from chucua_backend.dominio.humedal_puntos import PuntoHumedal
from chucua_backend.dominio.jac import JuntaAccionComunal
from chucua_backend.dominio.salud import CentroSalud
from chucua_backend.dominio.seguridad import PuntoSeguridad
from chucua_backend.dominio.servicios_publicos import PuntoServicioPublico
from chucua_backend.dominio.transporte import ParaderoSitp
from chucua_backend.dominio.via import EstadoVia
from chucua_backend.dominio.zonas_verdes import ZonaVerde

ESPECIFICACIONES = {
    "escenarios": (EscenarioDeportivo, ("tipo_escenario",)),
    "educativos": (CentroEducativo, ("nivel_educativo", "naturaleza")),
    "vias": (EstadoVia, ("tipo_via", "estado")),
    "catastro": (InformacionCatastral, ("uso_suelo", "area_m2")),
    "jac": (
        JuntaAccionComunal,
        ("presidente_contacto", "direccion", "horario_atencion"),
    ),
    "centros_salud": (
        CentroSalud,
        ("tipo_centro", "nivel_atencion", "horario", "direccion"),
    ),
    "seguridad": (PuntoSeguridad, ("tipo_punto", "cuadrante", "telefono_contacto")),
    "humedal_puntos": (
        PuntoHumedal,
        ("zona_humedal", "estado_conservacion", "especie_destacada"),
    ),
    "transporte": (
        ParaderoSitp,
        (
            "codigo_paradero",
            "rutas_alimentadoras",
            "direccion",
            "estado_senalizacion",
        ),
    ),
    "comercio": (
        ComercioLocal,
        ("categoria_comercial", "nombre_establecimiento", "direccion", "horario"),
    ),
    "cultura": (
        EspacioCultural,
        ("tipo_espacio", "actividad_principal", "direccion", "aforo_aproximado"),
    ),
    "servicios_publicos": (
        PuntoServicioPublico,
        ("tipo_servicio", "estado_operativo", "ubicacion_referencia"),
    ),
    "zonas_verdes": (
        ZonaVerde,
        ("area_aprox_m2", "tipo_vegetacion", "estado_mantenimiento", "direccion"),
    ),
    "demografia": (
        DemografiaSector,
        (
            "poblacion_estimada",
            "hogares_aprox",
            "grupo_etario_predominante",
            "anio_censo",
        ),
    ),
}

DOMINIOS = tuple(ESPECIFICACIONES)
