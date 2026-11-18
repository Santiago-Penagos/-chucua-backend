from ..dominio.salud import CentroSalud
from .servicio_base import ServicioBase


class ServicioCentrosSalud(ServicioBase[CentroSalud]):
    """Servicio de aplicación para centros de salud."""
