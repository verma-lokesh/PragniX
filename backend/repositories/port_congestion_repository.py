from models.port_congestion import PortCongestion
from repositories.base import BaseRepository


class PortCongestionRepository(BaseRepository[PortCongestion]):
    model = PortCongestion
