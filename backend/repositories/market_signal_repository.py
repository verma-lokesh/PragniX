from models.market_signal import MarketSignal
from repositories.base import BaseRepository


class MarketSignalRepository(BaseRepository[MarketSignal]):
    model = MarketSignal
