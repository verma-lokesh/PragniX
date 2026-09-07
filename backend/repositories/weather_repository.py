from models.weather import Weather
from repositories.base import BaseRepository


class WeatherRepository(BaseRepository[Weather]):
    model = Weather
