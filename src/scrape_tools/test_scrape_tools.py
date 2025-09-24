import pytest
from bs4 import BeautifulSoup
from src.scrape_tools.scrape_tools import (
    mut_filter_soup,
    get_text,
    fetch_raw_bytes,
    get_links,
    get_all_text,
)
from mock import patch, AsyncMock
from unittest.mock import patch
from aiohttp import ClientSession

link = "https://somelink.com"
html = f"""<html><script></script><div>asd</div><a href="{link}"></a><style></style><input><img></html>"""
parser = "html.parser"
bbytes = b"ASd"


def soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, parser)


def test_mut_filter_soup():
    actual = soup(html)

    mut_filter_soup(actual)

    expected = soup(f"""<html><div>asd</div><a href="{link}"></html>""")

    assert actual == expected


@pytest.mark.asyncio
async def mock_fetch_raw_bytes(*args) -> bytes:
    return f"{html}".encode("utf-8")


@pytest.mark.asyncio
async def test_get_text():
    with patch(
        "src.scrape_tools.scrape_tools.fetch_raw_bytes", new=mock_fetch_raw_bytes
    ):
        expected = "asd"
        actual = await get_text("url")
        assert actual == expected


class MockResponse:
    def __init__(self, data: bytes = b""):
        self._data = data

    async def read(self):
        return self._data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.mark.asyncio
async def test_fetch_raw_bytes():
    with patch.object(ClientSession, "get", return_value=MockResponse(bbytes)):
        actual = await fetch_raw_bytes("url")
        expected = bbytes
        assert actual == expected


@pytest.mark.asyncio
async def test_get_links():
    with patch(
        "src.scrape_tools.scrape_tools.fetch_raw_bytes", new=mock_fetch_raw_bytes
    ):
        expected = [link]
        actual = await get_links("url")
        assert expected == actual


texts = ["text1", "text2"]


@pytest.mark.asyncio
async def mock_gather(*args):
    return texts


@pytest.mark.asyncio
async def test_get_all_text():
    input = [link, link]
    expected = texts

    with patch("asyncio.gather", wraps=mock_gather) as gat:
        actual = await get_all_text(input)
        gat.assert_called_once()

        assert actual == expected
