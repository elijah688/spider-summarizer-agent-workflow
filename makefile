.PHONY: run

run:
	uv run python main.py

test:
	export PYTHONPATH=.;\
	uv run pytest  --capture=tee-sys

install:
	uv sync --locked
