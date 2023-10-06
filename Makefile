.DEFAULT_GOAL := all

.PHONY: build
build:
	RUSTFLAGS="--cfg uuid_unstable" maturin develop --release

.PHONY: format
format:
	ruff --fix python/ tests/
	black python/ tests/
	cargo fmt

.PHONY: lint
lint:
	ruff python/ tests/
	black --check --diff python/ tests/
	mypy python/ tests/
.PHONY: test
test:
	pytest tests -vvv


.PHONY: bench
bench:
	richbench benchmarks/

.PHONY: all
all: format build lint test
