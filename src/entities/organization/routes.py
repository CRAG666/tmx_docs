from src.shared.base_controller import ControllerBuilder
from src.shared.base_repository import BaseRepository
from .repository import OrganizationRepository
from .models import (
    Organization,
)
from .schemes import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationPublic,
)

# Inicializar el repositorio
organization_repository = OrganizationRepository(model=Organization)

# Inicializar el controlador
organization_controller = ControllerBuilder(
    repository=organization_repository,
    path_name="organization",
    response_schema=OrganizationPublic,
).enable_full_crud()
