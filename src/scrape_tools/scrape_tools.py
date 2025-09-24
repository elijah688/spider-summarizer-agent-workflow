import aiohttp
from bs4 import BeautifulSoup, Tag
import asyncio


async def __get_filtered_soup(w: str) -> BeautifulSoup:
    b = await fetch_raw_bytes(w)
    soup = BeautifulSoup(b, "html.parser")
    mut_filter_soup(soup)
    return soup


def mut_filter_soup(soup: BeautifulSoup):
    for t in ["script", "input", "img", "style"]:
        for x in soup.find_all(t):
            x.extract()


async def get_text(w: str) -> str:
    soup = await __get_filtered_soup(w)
    return soup.get_text(separator="\n", strip=True)


async def fetch_raw_bytes(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


async def get_links(w: str) -> list[str]:
    soup = await __get_filtered_soup(w)
    links = []
    for a in soup.find_all("a"):
        if isinstance(a, Tag):
            href = a.attrs["href"]
            links.append(href)

    return links


async def get_all_text(clean_links: list[str]) -> list[str]:
    coros = [asyncio.create_task(get_text(link)) for link in clean_links]
    return await asyncio.gather(*coros)
