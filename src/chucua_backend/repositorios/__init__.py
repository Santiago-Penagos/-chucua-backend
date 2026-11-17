from .catastro import RepositorioCatastro
from .contrato import IRepositorioCRUD
from .educativos import RepositorioEducativos
from .escenarios import RepositorioEscenarios
from .vias import RepositorioVias

__all__ = [
    "IRepositorioCRUD",
    "RepositorioEscenarios",
    "RepositorioEducativos",
    "RepositorioVias",
    "RepositorioCatastro",
]
