from src.shared.base_controller import ControllerBuilder
from src.shared.base_repository import BaseRepository

from .models import State
from .schemes import StatePublic

state_repository = BaseRepository[State, StatePublic, StatePublic](model=State)

state_controller = ControllerBuilder(
    repository=state_repository, path_name="state", response_schema=StatePublic
).enable_read_only()
