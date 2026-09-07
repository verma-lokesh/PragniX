from models.vessel import Vessel
from repositories.base import BaseRepository


class VesselRepository(BaseRepository[Vessel]):
    model = Vessel
