from models.recommendation import Recommendation
from repositories.base import BaseRepository


class RecommendationRepository(BaseRepository[Recommendation]):
    model = Recommendation
