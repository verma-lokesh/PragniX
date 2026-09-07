from models.market_entry import MarketEntry
from repositories.base import BaseRepository


class MarketEntryRepository(BaseRepository[MarketEntry]):
    model = MarketEntry
