.DEFAULT_GOAL := all

.PHONY: build
build:
	RUSTFLAGS="--cfg uuid_unstable" maturin develop --release

.PHONY: format
format:
	ruff check --fix python/ tests/
	ruff format python/ tests/
	cargo fmt

.PHONY: lint
lint:
	ruff check python/ tests/
	ruff format --check --diff python/ tests/
	mypy python/ tests/
.PHONY: test
test:
	pytest tests -vvv


.PHONY: bench
bench:
	richbench benchmarks/

.PHONY: all
all: format build lint test
