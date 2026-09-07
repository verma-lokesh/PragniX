from models.commodity import Commodity
from repositories.base import BaseRepository


class CommodityRepository(BaseRepository[Commodity]):
    model = Commodity
