from models.freight_rate import FreightRate
from repositories.base import BaseRepository


class FreightRateRepository(BaseRepository[FreightRate]):
    model = FreightRate
