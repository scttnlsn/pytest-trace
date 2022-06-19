import json
import os

import pytest_trace.plugin


def test_basic_span(testdir):
    test_code = """
        def add(x, y):
            return x + y

        def test_add():
            res = add(1, 2)
            assert res == 3
    """
    test_file = testdir.makepyfile(test_code)
    result = testdir.runpytest("--save-spans=spans.json", test_file)
    assert result.ret == 0

    data = _read_spans(testdir)

    assert len(data["spans"]) == 1
    span = data["spans"][0]
    assert span["name"] == "test"
    assert span["attributes"]["test.path"] == "test_basic_span.py"
    assert span["attributes"]["test.name"] == "test_add"
    assert span["attributes"]["test.line"] == 3


def test_nested_span(testdir):
    test_code = """
        from opentelemetry import trace

        tracer = trace.get_tracer(__name__)

        def add(x, y):
            with tracer.start_as_current_span("add") as span:
                span.set_attribute("x", x)
                span.set_attribute("y", y)
                res = x + y
            return res

        def test_add():
            res = add(1, 2)
            assert res == 3
    """
    test_file = testdir.makepyfile(test_code)
    result = testdir.runpytest("--save-spans=spans.json", test_file)
    assert result.ret == 0

    data = _read_spans(testdir)

    assert len(data["spans"]) == 3
    add_span = data["spans"][0]
    assert add_span["name"] == "add"
    assert add_span["attributes"]["x"] == 1
    assert add_span["attributes"]["y"] == 2
    test_span = data["spans"][1]
    assert test_span["name"] == "test"
    assert add_span["parent_id"] == test_span["context"]["span_id"]


def _read_spans(testdir, path="spans.json"):
    spans_path = os.path.join(str(testdir), path)
    with open(spans_path) as f:
        data = json.load(f)
    return data
