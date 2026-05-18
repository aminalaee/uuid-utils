.DEFAULT_GOAL := all

.PHONY: build
build:
	maturin develop --release

.PHONY: format
format:
	ruff format python/ tests/
	ruff check --fix python/ tests/
	cargo fmt

.PHONY: lint
lint:
	ruff check python/ tests/
	ruff format --check --diff python/ tests/
	ty check python/ tests/
.PHONY: test
test:
	pytest tests -vvv

.PHONY: bench
bench:
	benchdiff benchmarks/ --repeat 10 --times 100000

.PHONY: bench-report
bench-report:
	benchdiff benchmarks/bench_report.py --repeat 10 --times 100000 --svg docs/benchmarks.svg
	benchdiff benchmarks/bench_report.py --repeat 10 --times 100000

.PHONY: docs_build
docs_build:
	zensical build

.PHONY: docs_serve
docs_serve:
	zensical serve --dev-addr localhost:8080

.PHONY: all
all: format build lint test
