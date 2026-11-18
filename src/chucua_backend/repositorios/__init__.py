from .catastro import RepositorioCatastro
from .centros_salud import RepositorioCentrosSalud
from .comercio import RepositorioComercio
from .contrato import IRepositorioCRUD
from .cultura import RepositorioCultura
from .demografia import RepositorioDemografia
from .educativos import RepositorioEducativos
from .escenarios import RepositorioEscenarios
from .generico import RepositorioGenerico
from .humedal_puntos import RepositorioHumedalPuntos
from .jac import RepositorioJac
from .seguridad import RepositorioSeguridad
from .servicios_publicos import RepositorioServiciosPublicos
from .transporte import RepositorioTransporte
from .vias import RepositorioVias
from .zonas_verdes import RepositorioZonasVerdes

__all__ = [
    "IRepositorioCRUD",
    "RepositorioGenerico",
    "RepositorioEscenarios",
    "RepositorioEducativos",
    "RepositorioVias",
    "RepositorioCatastro",
    "RepositorioJac",
    "RepositorioCentrosSalud",
    "RepositorioSeguridad",
    "RepositorioHumedalPuntos",
    "RepositorioTransporte",
    "RepositorioComercio",
    "RepositorioCultura",
    "RepositorioServiciosPublicos",
    "RepositorioZonasVerdes",
    "RepositorioDemografia",
]
