from src.workflow.workflow import Workflow
from src.curator.curator import Curator
from src.writer.writer import Writer
import asyncio
from agents import trace

async def run():
    w = Writer()
    c = Curator()
    w = Workflow(c, w)
    with trace("Summarizer flow"):
       await w.run("https://www.anthropic.com")


if __name__ == "__main__":
    asyncio.run(run())
