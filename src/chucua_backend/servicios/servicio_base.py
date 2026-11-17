from typing import Generic

from ..errores import EntidadNoEncontrada
from ..repositorios.contrato import IRepositorioCRUD, T


class ServicioBase(Generic[T]):
    """Orquesta el CRUD delegando en el contrato inyectado."""

    def __init__(self, repositorio: IRepositorioCRUD[T]):
        self._repositorio = repositorio

    def crear(self, entidad: T) -> T:
        return self._repositorio.crear(entidad)

    def obtener(self, entidad_id: int) -> T:
        entidad = self._repositorio.obtener(entidad_id)
        if entidad is None:
            raise EntidadNoEncontrada(f"Entidad con id {entidad_id} no existe")
        return entidad

    def listar(self, sector: str | None = None) -> list[T]:
        return self._repositorio.listar(sector)

    def actualizar(self, entidad_id: int, entidad: T) -> T:
        return self._repositorio.actualizar(entidad_id, entidad)

    def eliminar(self, entidad_id: int) -> bool:
        return self._repositorio.eliminar(entidad_id)
