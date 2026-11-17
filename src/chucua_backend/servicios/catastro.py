from ..dominio.catastro import InformacionCatastral
from .servicio_base import ServicioBase


class ServicioCatastro(ServicioBase[InformacionCatastral]):
    """Servicio de aplicación para la información catastral."""
