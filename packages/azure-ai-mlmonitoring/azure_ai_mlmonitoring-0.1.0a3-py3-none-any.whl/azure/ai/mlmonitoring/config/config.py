# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=global-statement
import os
import json

from ..logger import is_debug, logger

default_queue_capacity = 100
default_worker_count = 1
default_sample_rate = 100


class MdcConfig:

    # pylint: disable=too-many-instance-attributes
    def __init__(
            self,
            enabled=False,
            host="127.0.0.1",
            port=50011,
            debug=False,
            sample_rate=default_sample_rate,
            model_version=None,
            queue_capacity=default_queue_capacity,
            worker_disabled=False,
            worker_count=default_worker_count,
            use_printer=False,
            compact_format=False,
    ):
        self._debug = debug
        self._enabled = enabled
        self._sample_rate = sample_rate
        self._host = host
        self._port = port
        self._model_version = model_version
        # queue - max length
        self._queue_capacity = queue_capacity
        # worker - disabled for test purpose only
        self._worker_disabled = worker_disabled
        self._worker_count = worker_count
        # payload sender
        self._use_printer = use_printer
        self._compact_format = compact_format

    def is_debug(self):
        return self._debug

    def enabled(self):
        return self._enabled

    def compact_format(self):
        return self._compact_format

    def sample_rate(self):
        return self._sample_rate

    def host(self):
        return self._host

    def port(self):
        return self._port

    def model_version(self):
        return self._model_version

    def queue_capacity(self):
        return self._queue_capacity

    def worker_disabled(self):
        return self._worker_disabled

    def worker_count(self):
        return self._worker_count

    def use_printer(self):
        return self._use_printer


def loadConfig(model_version=None):
    debug = is_debug()
    enabled = os.getenv("AZUREML_MDC_ENABLED", "false")
    if enabled.lower() == "true":
        return MdcConfig(
            enabled=True,
            host=os.getenv("AZUREML_MDC_HOST", "127.0.0.1"),
            port=int(os.getenv("AZUREML_MDC_PORT", "50011")),
            debug=debug,
            sample_rate=int(os.getenv("AZUREML_MDC_SAMPLE_RATE", str(default_sample_rate))),
            queue_capacity=int(os.getenv("AZUREML_MDC_QUEUE_CAPACITY", str(default_queue_capacity))),
            worker_disabled=os.getenv("AZUREML_MDC_WORKER_DISABLED", "false").lower() == "true",
            worker_count=int(os.getenv("AZUREML_MDC_WORKER_COUNT", str(default_worker_count))),
            compact_format=os.getenv("AZUREML_MDC_FORMAT_COMPACT", "false").lower() == "true",
            use_printer=os.getenv("AZUREML_MDC_WORKER_PRINTONLY", "false").lower() == "true",
            model_version=model_version,
        )

    return MdcConfig(enabled=False, debug=debug)


mdc_config = None


def init_config(model_version=None):
    global mdc_config
    mdc_config = loadConfig(model_version)

    logger.info("mdc enabled: %r", mdc_config.enabled())
    logger.info("mdc host: %s", mdc_config.host())
    logger.info("mdc port: %d", mdc_config.port())
    logger.info("mdc debugging: %r", mdc_config.is_debug())
    logger.info("mdc sample rate: %d", mdc_config.sample_rate())
    logger.info("mdc queue capacity: %d", mdc_config.queue_capacity())
    logger.info("mdc worker count: %d", mdc_config.worker_count())
    logger.info("mdc compact format: %r", mdc_config.compact_format())

    if mdc_config.is_debug():
        config_json = json.dumps(mdc_config.__dict__)
        logger.debug("mdc config: %s", config_json)


def teardown_config():
    global mdc_config
    mdc_config = None


def get_config():
    global mdc_config
    return mdc_config
