from models.freight_forecast import FreightForecast
from repositories.base import BaseRepository


class FreightForecastRepository(BaseRepository[FreightForecast]):
    model = FreightForecast
