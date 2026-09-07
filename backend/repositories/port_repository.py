from models.port import Port
from repositories.base import BaseRepository


class PortRepository(BaseRepository[Port]):
    model = Port
