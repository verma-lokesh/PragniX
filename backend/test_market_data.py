from core.services.market_data_service import MarketDataService


service = MarketDataService()

news = service.collect_market_news()

print(f"\nTotal results: {len(news)}")

for item in news[:10]:

    print("\n==============================")
    print("QUERY:", item["query"])
    print("TITLE:", item["title"])
    print("URL:", item["url"])
    print("CONTENT:", item["content"][:300])