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

.PHONY: docs_build
docs_build:
	mkdocs build

.PHONY: docs_serve
docs_serve:
	mkdocs serve --dev-addr localhost:8080

.PHONY: docs_deploy
docs_deploy:
	mkdocs gh-deploy --force

.PHONY: all
all: format build lint test
