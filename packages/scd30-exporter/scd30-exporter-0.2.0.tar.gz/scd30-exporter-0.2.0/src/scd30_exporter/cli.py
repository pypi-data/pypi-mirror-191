# MIT license
# Copyright 2023 Sergej Alikov <sergej@alikov.com>

import argparse
import importlib.metadata
import logging
import time

import adafruit_scd30  # type: ignore
import board  # type: ignore
import busio  # type: ignore
from prometheus_client import Gauge, Summary, start_http_server

logger = logging.getLogger(__name__)

METRIC_MEASUREMENT_TIME = Summary(
    "scd30_measurement_seconds", "Time spent processing performing measurement"
)
METRIC_SENSOR_CO2 = Gauge("scd30_sensor_co2", "CO2 (PPM)", ["sensor"])
METRIC_SENSOR_TEMPERATURE = Gauge(
    "scd30_sensor_temperature", "Temperature (degrees C)", ["sensor"]
)
METRIC_SENSOR_HUMIDITY = Gauge("scd30_sensor_humidity", "Humidity (%%rH)", ["sensor"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="scd30-exporter",
        description=importlib.metadata.metadata("scd30-exporter")["Summary"],
    )

    parser.add_argument("name", help="sensor name")

    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"),
        help="log level",
    )

    parser.add_argument(
        "--interval", type=int, default=10, help="interval in seconds between readings"
    )

    parser.add_argument("--port", type=int, default=8000, help="exporter port")

    return parser.parse_args()


@METRIC_MEASUREMENT_TIME.time()
def read_data(scd: adafruit_scd30.SCD30) -> tuple:
    while True:
        if scd.data_available:
            return scd.CO2, scd.temperature, scd.relative_humidity

        time.sleep(0.5)


def main() -> None:

    args = parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=args.log_level,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    start_http_server(args.port)

    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)

    while True:
        co2, temp, humidity = read_data(scd)
        logger.debug(
            f"CO2: {co2:.2f} PPM, Temperature: {temp:.2f} °C, Humidity: {humidity:.2f} %%rH"
        )
        METRIC_SENSOR_CO2.labels(args.name).set(co2)
        METRIC_SENSOR_TEMPERATURE.labels(args.name).set(temp)
        METRIC_SENSOR_HUMIDITY.labels(args.name).set(humidity)

        time.sleep(args.interval)
