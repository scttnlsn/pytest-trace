# pytest-trace

[![tests](https://github.com/scttnlsn/pytest-trace/actions/workflows/tests.yml/badge.svg)](https://github.com/scttnlsn/pytest-trace/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/pytest-trace.svg)](https://pypi.org/project/pytest-trace/)

Save [OpenTelemetry](https://opentelemetry.io/) spans generated during testing

## Install

```
pip install pytest-trace
```

## Usage

```
pytest --save-spans=spans.json
```