import pytest
from openai.types.responses import ResponseTextDeltaEvent


class MockOpen:
    def __init__(self, *args, **kwargs):
        self.file = self
        self.buffered_output = ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, s):
        self.buffered_output += s

    def flush(self):
        pass


@pytest.mark.asyncio
async def mock_stream_events(runner_chunks):
    for chunk in runner_chunks:

        class Event:
            type = "raw_response_event"
            data = ResponseTextDeltaEvent(
                type="response.output_text.delta",
                content_index=1,
                delta=chunk,
                item_id="1",
                logprobs=[],
                output_index=1,
                sequence_number=1,
            )

        yield Event()


class MockRunResult:
    def __init__(self, final_output):
        self.final_output = final_output
