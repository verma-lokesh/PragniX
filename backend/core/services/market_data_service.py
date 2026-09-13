from core.services.web_search.tavily_client import TavilySearchProvider


class MarketDataService:

    def __init__(self):
        self.tavily = TavilySearchProvider()

    def collect_market_news(self):

        queries = [
            "Baltic Dry Index latest freight market",
            "Baltic Capesize Index latest",
            "Baltic Panamax Index latest",
            "dry bulk shipping freight rates",
            "China iron ore imports shipping demand",
            "China coal imports dry bulk shipping",
            "global dry bulk shipping demand",
            "port congestion dry bulk shipping",
            "Red Sea shipping disruption",
            "Panama Canal shipping restrictions",
        ]

        all_results = []

        for query in queries:

            results = self.tavily.search(
                query=query,
                max_results=5
            )

            for result in results:

                all_results.append({
                    "query": query,
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                })

        return all_results