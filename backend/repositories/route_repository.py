from models.route import Route
from repositories.base import BaseRepository


class RouteRepository(BaseRepository[Route]):
    model = Route
