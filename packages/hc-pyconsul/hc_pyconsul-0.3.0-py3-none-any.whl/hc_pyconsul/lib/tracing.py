import functools

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


def tracing(name):
    """Used to instrument pieces of the library with OpenTelemetry"""

    def outter_wrap(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with tracer.start_as_current_span(name=f'Consul - {name}', kind=trace.SpanKind.CLIENT) as span:

                try:
                    results = func(self, *args, **kwargs)
                except Exception as func_error:
                    error = trace.status.Status(trace.status.StatusCode.ERROR)
                    span.record_exception(exception=func_error)
                    span.set_status(error)
                    raise func_error
                return results

        return wrapper

    return outter_wrap
