from models.simulation import Simulation
from repositories.base import BaseRepository


class SimulationRepository(BaseRepository[Simulation]):
    model = Simulation
