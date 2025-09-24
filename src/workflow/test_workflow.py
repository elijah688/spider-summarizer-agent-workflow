import pytest
from src.workflow.workflow import Workflow
from src.curator.curator import Curator
from src.writer.writer import Writer
from mock import patch, MagicMock
from src.model.model import LinksList
from testing.mocks import mock_stream_events, MockRunResult, MockOpen

URL = "https://anthropic.com"

RELEVANT_LINKS = [f"{URL}/about", f"{URL}/pricing", "", f"{URL}/funny#what"]
TEXTS = ["TEXT1", "TEXT2"]
CHUNKS = ["Hello ", "world", "!"]


@pytest.mark.asyncio
async def test_workflow():
    w = Writer()
    c = Curator()
    w = Workflow(c, w)
    m = MockOpen()

    mock_runner_obj = MagicMock()
    mock_runner_obj.stream_events = lambda *args, **kwargs: mock_stream_events(CHUNKS)

    with (
        patch(
            "src.curator.curator.get_links", return_value=RELEVANT_LINKS
        ) as mock_get_links_patch,
        patch(
            "src.curator.curator.Runner.run",
            return_value=MockRunResult(LinksList(links=RELEVANT_LINKS)),
        ) as mock_run_patch,
        patch(
            "src.workflow.workflow.get_all_text", return_value=TEXTS
        ) as mock_get_links_patch,
        patch("os.makedirs", return_value=None) as makedirs_patch,
        patch("builtins.open", return_value=m) as open_patch,
        patch("src.writer.writer.Runner.run_streamed", return_value=mock_runner_obj) as run_stream_patch,
    ):
        await w.run(URL)

        mock_get_links_patch.assert_called_once()
        mock_run_patch.assert_called_once()
        makedirs_patch.assert_called_once()
        open_patch.assert_called_once()
        run_stream_patch.assert_called_once()

        assert m.buffered_output == "".join(CHUNKS)
