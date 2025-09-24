## Overview

This project provides a workflow to **curate links from a website, gather text content, and generate a structured report**. It leverages three main components:

* **Curator** – identifies and filters the most relevant links from a target website.
* **Writer** – generates a report based on curated content.
* **Workflow** – orchestrates the full pipeline from scraping links to producing the report.

The workflow is designed to be asynchronous, making it efficient for web scraping and report generation.

---

## Requirements

* Python 3.13+
* `asyncio`
* `pytest` for testing
* `uv` for running commands (make sure `uv` CLI is installed)

Other dependencies are included in `agents`, `src.scrape_tools`, and your model packages (`gpt-5-nano`, `gpt-4.1`).

---

## Installation

```bash
git clone <repo_url>
cd <repo_directory>
make install
```

---

## Running the Workflow

You can run the main workflow using the provided `main.py` script:

```bash
make run
```

This will:

1. Initialize the `Curator` and `Writer`.
2. Run the `Workflow` with a given URL.
3. Produce a report using the `Writer` and print a trace log of the workflow.

The default report save to location is:

```
output/company_report.md
```

You can override these defaults with environment variables:

```bash
export OUTPUT_DIR="my_reports"
export FILENAME="custom_report.md"
```

---

## Makefile Commands

You can also use the included Makefile:

```bash
make run       # Runs the main.py workflow
make test      # Runs pytest and captures output
make install   # Brings in all necessary project dependencies
```

---

## Testing

Tests use `pytest` with async support. Example:

```bash
make test
```

Tests include:

* Mocking network calls and scraping.
* Capturing streamed output from the Writer.
* Ensuring that generated reports match expected content.

---

## Project Structure

```
src/
├─ curator/
│  └─ curator.py      # Curator class for filtering relevant links
├─ writer/
│  └─ writer.py       # Writer class for generating reports
├─ workflow/
│  └─ workflow.py     # Workflow orchestrator
├─ scrape_tools/
│  └─ scrape_tools.py # Helpers for scraping web content
main.py               # Entry point script
Makefile              # For running commands
tests/                # Test classes and utils
```

---

## Example Usage

```python
from src.workflow.workflow import Workflow
from src.curator.curator import Curator
from src.writer.writer import Writer
import asyncio
from agents import trace

async def run():
    w = Writer()
    c = Curator()
    workflow = Workflow(c, w)

    with trace("Summarizer flow"):
        await workflow.run("https://www.anthropic.com/")

asyncio.run(run())
```

This runs the full pipeline: fetch links → extract content → generate report.