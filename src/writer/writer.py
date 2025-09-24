from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
import os
from src.instructions.instructions import writer


class Writer:
    def __init__(self):
        self.agent = Agent(
            name="Brochure Writer",
            instructions=writer,
            model="gpt-4.1",
        )

    def __generate_agent_input(self, url: str, texts: list[str]):
        return f"Create a report for the company {url}.\nHere's the info we compiled on them:\n{'\n'.join(texts)}"

    async def generate_report(self, url: str, texts: list[str]):
        output_dir = os.environ.get("OUTPUT_DIR", "output")
        filename = os.environ.get("FILENAME", "company_report.md")

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            w_res = Runner.run_streamed(
                self.agent, input=self.__generate_agent_input(url, texts)
            )

            async for event in w_res.stream_events():
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    chunk = event.data.delta
                    f.write(chunk)
                    f.flush()

        print(f"Report saved to {file_path}")
