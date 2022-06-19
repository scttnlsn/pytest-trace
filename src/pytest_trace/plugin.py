import json
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

exporter = InMemorySpanExporter()
processor = SimpleSpanProcessor(exporter)

provider = TracerProvider()
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


def pytest_addoption(parser):
    group = parser.getgroup("trace", "trace options")
    group.addoption("--save-spans", help="store spans to given file path")


def pytest_runtest_call(item):
    path, line, name = item.reportinfo()
    cwd = os.getcwd()
    relpath = os.path.relpath(path, cwd)

    with tracer.start_as_current_span("test") as span:
        span.set_attribute("test.path", relpath)
        span.set_attribute("test.name", name)
        span.set_attribute("test.line", line)
        item.runtest()


def pytest_sessionfinish(session, exitstatus):
    spans_path = session.config.option.save_spans
    if spans_path:
        spans = [json.loads(span.to_json()) for span in exporter.get_finished_spans()]
        with open(spans_path, "w") as f:
            json.dump({"spans": spans}, f, indent=4)
