import logger
from random import randint
from flask import Flask

from opentelemetry import trace, metrics


app = Flask(__name__)

@app.route("/rolldice")
def roll_dice():
    logger.info("I'm rolling some dice here!")
    res = ""
    try:
        res = str(do_roll())
    except Exception as e:
        res = "0"
        with tracer.start_as_current_span("odd_number") as span:
            span.record_exception(e)
            print(f"PRINT: Returning value {res} from exception {str(e)}")
            logger.error(f"Uh-oh. We have an exception. Returning {res}")
        
    return res

def do_roll():
    res = randint(1, 6)

    # By default, record_exception is True. If we set it to false, it still creates a Span Event, but not one with the full exception.
    with tracer.start_as_current_span("do_roll", set_status_on_exception=True, kind=trace.SpanKind.SERVER) as span:
        span = trace.get_current_span()
        span.set_attribute("roll.value", res)
        # span.set_status(trace.StatusCode.ERROR)
        
        # Add attributes for span event
        attributes = {}
        attributes["key1"] = "value1"
        attributes["key2"] = "value2"

        span.add_event("This is a span event", attributes=attributes)

        logger.info("This is a log message!!")

        request_counter.add(1)
        
        if (res % 2 == 0):
            raise Exception("Divisible by 2!")

    return res

if __name__ == "__main__":
    # Init tracer
    tracer = trace.get_tracer_provider().get_tracer(__name__)

    # Init metrics + create a counter instrument
    meter = metrics.get_meter_provider().get_meter(__name__)
    request_counter = meter.create_counter(name="request_counter", description="Number of requests", unit="1")

    # Init logs
    logger = logger.init_logger()

    app.run(host="0.0.0.0", port=8082, debug=True, use_reloader=False)