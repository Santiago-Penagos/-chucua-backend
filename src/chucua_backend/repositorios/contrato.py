from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class IRepositorioCRUD(Protocol[T]):
    """Contrato de persistencia que deben cumplir todos los dominios."""

    def crear(self, entidad: T) -> T: ...

    def obtener(self, entidad_id: int) -> T | None: ...

    def listar(self, sector: str | None = None) -> list[T]: ...

    def actualizar(self, entidad_id: int, entidad: T) -> T: ...

    def eliminar(self, entidad_id: int) -> bool: ...

    def upsert_por_osm_id(self, entidad: T) -> T: ...
