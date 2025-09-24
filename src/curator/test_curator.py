import pytest
from src.curator.curator import Curator
from mock import patch
from agents import Runner
from src.model.model import LinksList
from testing.mocks import MockRunResult

url = "http://anthropic.com"
relevant_links = [f"{url}/about", f"{url}/pricing", "", f"{url}/funny#what"]


@pytest.mark.asyncio
async def mock_run(*args) -> MockRunResult:
    return MockRunResult(LinksList(links=relevant_links))


@pytest.mark.asyncio
async def mock_get_links(*args) -> list[str]:
    return relevant_links


@pytest.mark.asyncio
async def test_get_relevant_link():
    expected = [
        "http://anthropic.com/about",
        "http://anthropic.com/pricing",
        "http://anthropic.com/funny",
    ]
    c = Curator()

    with (
        patch("src.curator.curator.get_links", wraps=mock_get_links) as mgl,
        patch.object(Runner, "run", wraps=mock_run) as mock_run_patch,
    ):
        actual = await c.get_relevant_links(url)

        mgl.assert_called_once()
        mock_run_patch.assert_called_once()
        assert actual == expected
