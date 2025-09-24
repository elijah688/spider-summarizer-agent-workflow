import os
import pytest
from mock import patch, MagicMock
from src.writer.writer import Writer

from testing.mocks import MockOpen, mock_stream_events


runner_chunks = ["Hello ", "world", "!"]


@pytest.mark.asyncio
async def test_generate_report():
    writer = Writer()
    test_url = "http://example.com"
    test_texts = ["Some", "text"]

    mock_runner_obj = MagicMock()
    mock_runner_obj.stream_events = lambda *args, **kwargs: mock_stream_events(
        runner_chunks
    )

    m = MockOpen()
    with (
        patch("os.makedirs") as mock_makedirs,
        patch("builtins.open", lambda *args, **kwargs: m),
        patch("src.writer.writer.Runner.run_streamed", return_value=mock_runner_obj),
    ):
        mock_makedirs.return_value = None

        await writer.generate_report(test_url, test_texts)

        mock_makedirs.assert_called_once_with(
            os.environ.get("OUTPUT_DIR", "output"), exist_ok=True
        )

        assert m.buffered_output == "".join(runner_chunks)
