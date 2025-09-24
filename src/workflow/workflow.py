from src.curator.curator import Curator
from src.writer.writer import Writer
from src.scrape_tools.scrape_tools import get_all_text

class Workflow:
    def __init__(self, c: Curator, w: Writer):
        self.curator = c
        self.writer = w

    async def run(self, url: str):
        links = await self.curator.get_relevant_links(url)
        all_texts = await get_all_text(links)
        await self.writer.generate_report(url, all_texts)
