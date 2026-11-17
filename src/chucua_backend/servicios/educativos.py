from ..dominio.educativo import CentroEducativo
from .servicio_base import ServicioBase


class ServicioEducativos(ServicioBase[CentroEducativo]):
    """Servicio de aplicación para centros educativos."""
