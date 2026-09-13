import os
from tavily import TavilyClient


class TavilySearchProvider:

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError("TAVILY_API_KEY is not configured")

        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5):

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
        )

        return response.get("results", [])
