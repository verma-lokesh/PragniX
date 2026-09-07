from models.bunker_price import BunkerPrice
from repositories.base import BaseRepository


class BunkerPriceRepository(BaseRepository[BunkerPrice]):
    model = BunkerPrice
