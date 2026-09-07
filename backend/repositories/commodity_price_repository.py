from models.commodity_price import CommodityPrice
from repositories.base import BaseRepository


class CommodityPriceRepository(BaseRepository[CommodityPrice]):
    model = CommodityPrice
