from src.shared.base_controller import ControllerBuilder
from src.shared.base_repository import BaseRepository
from .repository import UserRepository
from .models import (
    User,
    UserRole,
)
from .schemes import (
    UserCreate,
    UserUpdate,
    UserPublic,
    UserRolePublic,
)

# Inicializar el repositorio
user_repository = UserRepository(model=User)

user_controller = ControllerBuilder(
    repository=user_repository,
    path_name="users",
    response_schema=UserPublic,
).enable_full_crud(create_schema=UserCreate, update_schema=UserUpdate)

user_role_repository = BaseRepository[UserRole, UserRolePublic, UserRolePublic](
    model=UserRole
)

user_role_controller = ControllerBuilder(
    repository=user_role_repository,
    path_name="roles",
    response_schema=UserRolePublic,
).enable_read_only()
