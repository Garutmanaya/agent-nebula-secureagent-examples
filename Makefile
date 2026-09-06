.PHONY: install lint init clean

install:
	uv sync --group dev

lint:
	uv run ruff check examples

init:
	./scripts/init-all.sh

clean:
	./scripts/clean-all.sh
