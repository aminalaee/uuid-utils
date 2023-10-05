.DEFAULT_GOAL := all

.PHONY: build
build:
	RUSTFLAGS="--cfg uuid_unstable" maturin develop --release

.PHONY: format
format:
	ruff --fix python/
	black python/
	cargo fmt

.PHONY: lint
lint:
	ruff python/
	black --check --diff python/
	mypy python/

.PHONY: test
test:
	pytest tests -vvv


.PHONY: bench
bench:
	richbench benchmarks/

.PHONY: all
all: format build lint test
