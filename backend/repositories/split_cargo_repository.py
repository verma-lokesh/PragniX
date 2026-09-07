from models.split_cargo import SplitCargo
from repositories.base import BaseRepository


class SplitCargoRepository(BaseRepository[SplitCargo]):
    model = SplitCargo
