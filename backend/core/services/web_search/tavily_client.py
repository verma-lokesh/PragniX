from tavily import TavilyClient

from config.settings import get_settings


class TavilySearchProvider:

    def __init__(self):
        settings = get_settings()

        if not settings.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is not configured")

        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(self, query: str, max_results: int = 5):

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
        )

        return response.get("results", [])