import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx
import yaml
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from tenacity import retry, stop_after_attempt, wait_exponential



# LOGGING

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("universal-scraper")



# DATA MODELS


@dataclass
class ScrapedRecord:
    source: str
    source_type: str
    url: str
    scraped_at: str
    content_hash: str
    data: dict[str, Any]


@dataclass
class ScrapeResult:
    source: str
    url: str
    success: bool
    status_code: Optional[int]
    duration_ms: int
    records: list[ScrapedRecord]
    error: Optional[str] = None



# UNIVERSAL SCRAPER


class UniversalScraper:

    def __init__(
        self,
        output_dir: str = "output",
        timeout: int = 30,
        delay: float = 1.0,
    ):
        self.output_dir = Path(output_dir)
        self.raw_dir = self.output_dir / "raw"
        self.normalized_dir = self.output_dir / "normalized"

        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.normalized_dir.mkdir(parents=True, exist_ok=True)

        self.timeout = timeout
        self.delay = delay

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; FreightIntelligenceBot/1.0)"
            ),
            "Accept": "text/html,application/xhtml+xml",
        }

    # HTTP FETCH

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8,
        ),
    )
    async def fetch_http(
        self,
        url: str,
    ) -> tuple[str, int]:

        async with httpx.AsyncClient(
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        ) as client:

            response = await client.get(url)

            response.raise_for_status()

            return response.text, response.status_code

    
    # PLAYWRIGHT FETCH
    

    async def fetch_browser(
        self,
        url: str,
        selector: Optional[str] = None,
    ) -> tuple[str, int]:

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            page = await browser.new_page(
                user_agent=self.headers["User-Agent"]
            )

            response = await page.goto(
                url,
                wait_until="networkidle",
                timeout=self.timeout * 1000,
            )

            if selector:
                await page.wait_for_selector(
                    selector,
                    timeout=self.timeout * 1000,
                )

            html = await page.content()

            status_code = (
                response.status
                if response
                else 200
            )

            await browser.close()

            return html, status_code

    
    # SAVE RAW HTML
    

    def save_raw(
        self,
        source: str,
        html: str,
    ) -> str:

        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d_%H%M%S")

        filename = (
            f"{source}_{timestamp}.html"
        )

        path = self.raw_dir / filename

        path.write_text(
            html,
            encoding="utf-8",
        )

        return str(path)

    
    # HASH
    

    @staticmethod
    def generate_hash(
        data: Any,
    ) -> str:

        serialized = json.dumps(
            data,
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            serialized.encode()
        ).hexdigest()

    
    # TEXT EXTRACTION
    

    @staticmethod
    def extract_text(
        soup: BeautifulSoup,
        selector: str,
    ) -> str:

        element = soup.select_one(selector)

        if not element:
            return ""

        return element.get_text(
            " ",
            strip=True,
        )


    # ATTRIBUTE EXTRACTION


    @staticmethod
    def extract_attribute(
        soup: BeautifulSoup,
        selector: str,
        attribute: str,
    ) -> Optional[str]:

        element = soup.select_one(selector)

        if not element:
            return None

        return element.get(attribute)


    # TABLE EXTRACTION


    @staticmethod
    def extract_table(
        soup: BeautifulSoup,
        selector: str,
    ) -> list[dict[str, str]]:

        table = soup.select_one(selector)

        if not table:
            return []

        rows = table.select("tr")

        if not rows:
            return []

        headers = [
            cell.get_text(
                " ",
                strip=True,
            )
            for cell in rows[0].select(
                "th, td"
            )
        ]

        records = []

        for row in rows[1:]:

            cells = [
                cell.get_text(
                    " ",
                    strip=True,
                )
                for cell in row.select(
                    "td, th"
                )
            ]

            if not cells:
                continue

            record = {}

            for index, value in enumerate(cells):

                if index < len(headers):
                    record[
                        headers[index]
                    ] = value

            records.append(record)

        return records


    # GENERIC EXTRACTION

    def extract(
        self,
        html: str,
        config: dict[str, Any],
    ) -> list[dict[str, Any]]:

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        extraction_type = config.get(
            "type",
            "text",
        )

        selector = config.get(
            "selector"
        )

        
        # TABLE
        

        if extraction_type == "table":

            return self.extract_table(
                soup,
                selector,
            )

        
        # TEXT

        if extraction_type == "text":

            value = self.extract_text(
                soup,
                selector,
            )

            return [
                {
                    config.get(
                        "field",
                        "value",
                    ): value
                }
            ]

        
        # ATTRIBUTE
        

        if extraction_type == "attribute":

            value = self.extract_attribute(
                soup,
                selector,
                config["attribute"],
            )

            return [
                {
                    config.get(
                        "field",
                        "value",
                    ): value
                }
            ]

        
        # MULTIPLE ITEMS
        

        if extraction_type == "items":

            elements = soup.select(
                selector
            )

            records = []

            for element in elements:

                record = {}

                for field in config.get(
                    "fields",
                    [],
                ):

                    name = field["name"]
                    field_selector = field[
                        "selector"
                    ]

                    target = element.select_one(
                        field_selector
                    )

                    if target:

                        if field.get(
                            "attribute"
                        ):
                            value = target.get(
                                field["attribute"]
                            )
                        else:
                            value = target.get_text(
                                " ",
                                strip=True,
                            )

                    else:
                        value = None

                    record[name] = value

                records.append(record)

            return records

        raise ValueError(
            f"Unsupported extraction type: "
            f"{extraction_type}"
        )

    
    # SCRAPE ONE SOURCE
    

    async def scrape(
        self,
        source_config: dict[str, Any],
    ) -> ScrapeResult:

        source = source_config["name"]
        url = source_config["url"]

        start = time.perf_counter()

        logger.info(
            "Scraping %s → %s",
            source,
            url,
        )

        try:

            use_browser = source_config.get(
                "browser",
                False,
            )

            if use_browser:

                html, status_code = (
                    await self.fetch_browser(
                        url,
                        source_config.get(
                            "wait_for"
                        ),
                    )
                )

            else:

                html, status_code = (
                    await self.fetch_http(
                        url
                    )
                )

            # Save raw response
            raw_path = self.save_raw(
                source,
                html,
            )

            logger.info(
                "Raw HTML saved: %s",
                raw_path,
            )

            # Extract
            extraction_config = (
                source_config["extraction"]
            )

            extracted = self.extract(
                html,
                extraction_config,
            )

            timestamp = datetime.now(
                timezone.utc
            ).isoformat()

            records = []

            for item in extracted:

                record_hash = (
                    self.generate_hash(item)
                )

                record = ScrapedRecord(
                    source=source,
                    source_type="web_scrape",
                    url=url,
                    scraped_at=timestamp,
                    content_hash=record_hash,
                    data=item,
                )

                records.append(record)

            duration = int(
                (time.perf_counter() - start)
                * 1000
            )

            return ScrapeResult(
                source=source,
                url=url,
                success=True,
                status_code=status_code,
                duration_ms=duration,
                records=records,
            )

        except Exception as exc:

            duration = int(
                (time.perf_counter() - start)
                * 1000
            )

            logger.exception(
                "Scraping failed: %s",
                source,
            )

            return ScrapeResult(
                source=source,
                url=url,
                success=False,
                status_code=None,
                duration_ms=duration,
                records=[],
                error=str(exc),
            )

    
    # SAVE NORMALIZED RESULT

    def save_result(
        self,
        result: ScrapeResult,
    ):

        timestamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d_%H%M%S")

        path = (
            self.normalized_dir
            / f"{result.source}_{timestamp}.json"
        )

        payload = {
            "source": result.source,
            "url": result.url,
            "success": result.success,
            "status_code": result.status_code,
            "duration_ms": result.duration_ms,
            "error": result.error,
            "records": [
                asdict(record)
                for record in result.records
            ],
        }

        path.write_text(
            json.dumps(
                payload,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        logger.info(
            "Result saved: %s",
            path,
        )

    # RUN MULTIPLE SOURCES

    async def run(
        self,
        sources: list[dict[str, Any]],
    ):

        results = []

        for source in sources:

            result = await self.scrape(
                source
            )

            self.save_result(result)

            results.append(result)

            await asyncio.sleep(
                self.delay
            )

        return results


# CONFIG LOADER

def load_sources(
    path: str = "sources.yaml",
):

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        config = yaml.safe_load(file)

    return config["sources"]


# Main

async def main():

    sources = load_sources()

    scraper = UniversalScraper(
        output_dir="output",
        timeout=30,
        delay=2,
    )

    results = await scraper.run(
        sources
    )

    print("SCRAPING SUMMARY")

    for result in results:

        print(
            f"{result.source}: "
            f"{'SUCCESS' if result.success else 'FAILED'} "
            f"({len(result.records)} records)"
        )


if __name__ == "__main__":

    asyncio.run(main())