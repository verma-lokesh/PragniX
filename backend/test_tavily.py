from core.services.web_search.tavily_client import TavilySearchProvider


provider = TavilySearchProvider()

results = provider.search(
    "latest Baltic Dry Index freight shipping news",
    max_results=5
)

print("\n========== TAVILY RESULTS ==========\n")

for result in results:
    print("TITLE:", result.get("title"))
    print("URL:", result.get("url"))
    print("CONTENT:", result.get("content", "")[:500])
    print("------------------------------------")