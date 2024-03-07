# OTel Errors Example with Python

This is the companion repo for the [Observability Day EU 2024 Talk, "Dude, Where's My Error"](https://colocatedeventseu2024.sched.com/event/1YFeM/dude-wheres-my-error-how-opentelemetry-records-errors-and-why-it-does-it-like-that-adriana-villela-servicenow-cloud-observability-formerly-lightstep-reese-lee-new-relic).

## Quickstart

Check out the quickstart [here](./src/python/README.md), and check out the demo video [here](https://youtu.be/dRbUKhBtMg4), which shows you how to run this project in GitHub Codespaces.

## Additional Collector configs

If you'd like to send OpenTelemetry data to a different Observability backend, consider creating an `otelcol-config-extras.yml` file. It serves as an override/addendum file of Collector configs, whereby base configs are kept in `otelcol-config.yaml`.

You can find a sample [here](https://github.com/open-telemetry/opentelemetry-demo/blob/main/src/otelcollector/otelcol-config-extras.yml).