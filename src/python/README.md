# Python OTel Example

## Docker Compose

```bash
docker compose build
docker compose up
```

>**NOTE:** Use `--no-cache` to build without cached layers.

## Without Docker Compose

### Setup

Set up the Python virtual environment and install dependencies.

```bash
python3 -m venv src/python/venv
source src/python/venv/bin/activate

pip install --upgrade pip

# Installs dependencies
pip install -r src/python/requirements.txt
opentelemetry-bootstrap -a install
```

### Start OTel Collector

```
docker run -it --rm -p 4317:4317 -p 4318:4318 \
    -v $(pwd)/src/otelcollector/otelcol-config.yml:/etc/otelcol-config.yml \
    -v $(pwd)/src/otelcollector/otelcol-config-extras.yml:/etc/otelcol-config-extras.yml \
    --name otelcol otel/opentelemetry-collector-contrib:0.93.0  \
    "--config=/etc/otelcol-config.yml" "--config=/etc/otelcol-config-extras.yml"
```

### Start the Services

Open up a new terminal window and start the server:

```
# Version 1: Use Python log auto-instrumentation
source src/python/venv/bin/activate
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOG_LEVEL=debug
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp \
    --service_name test-py-server \
    python src/python/server.py


# Version 2: Don't use Python log auto-instrumentation
source src/python/venv/bin/activate
export OTEL_PYTHON_LOG_CORRELATION=true
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp \
    --service_name test-py-server \
    python src/python/server2.py
```

Open up a new terminal window and start the client:

```
source src/python/venv/bin/activate
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console,otlp \
    --logs_exporter console,otlp \
    --service_name test-py-client \
    python src/python/client.py
```

