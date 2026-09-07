from models.idle_vessel import IdleVessel
from repositories.base import BaseRepository


class IdleVesselRepository(BaseRepository[IdleVessel]):
    model = IdleVessel
