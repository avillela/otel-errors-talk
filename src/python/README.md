# Python OTel Example README

## Setup

```bash
python3 -m venv src/python/venv
source src/python/venv/bin/activate

pip install --upgrade pip

# Installs dependencies
pip install -r src/python/requirements.txt
opentelemetry-bootstrap -a install
```

## Docker Compose

```bash
docker compose -f docker-compose.yml --env-file .env build
docker compose -f docker-compose.yml --env-file .env up
```

>**NOTE:** Use `--no-cache` to build without cached layers.

## Without Docker Compose

### Start OTel Collector

```
docker run -it --rm -p 4317:4317 -p 4318:4318 \
    -v $(pwd)/src/otelcollector/otelcol-config.yml:/etc/otelcol-config.yml \
    -v $(pwd)/src/otelcollector/otelcol-config-extras.yml:/etc/otelcol-config-extras.yml \
    --name otelcol otel/opentelemetry-collector-contrib:0.93.0  \
    "--config=/etc/otelcol-config.yml" "--config=/etc/otelcol-config-extras.yml"
```

### Start the Services

Start server by opening up a new terminal window:

```
source src/python/venv/bin/activate
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_PYTHON_LOG_CORRELATION=true
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp \
    --service_name test-py-server \
    python src/python/server.py


# Other environment vars available for use
export OTEL_PYTHON_LOG_FORMAT="%(msg)s [span_id=%(span_id)s]"
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_LEVEL=debug
```

Start up client in a new terminal window:

```
source src/python/venv/bin/activate
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp \
    --service_name test-py-client \
    python src/python/client.py
```

