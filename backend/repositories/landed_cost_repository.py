from models.landed_cost import LandedCost
from repositories.base import BaseRepository


class LandedCostRepository(BaseRepository[LandedCost]):
    model = LandedCost
