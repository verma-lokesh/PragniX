from models.decision_request import DecisionRequest
from repositories.base import BaseRepository


class DecisionRequestRepository(BaseRepository[DecisionRequest]):
    model = DecisionRequest
