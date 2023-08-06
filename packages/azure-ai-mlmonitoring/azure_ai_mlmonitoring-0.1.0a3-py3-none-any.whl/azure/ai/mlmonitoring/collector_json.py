# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import sys
import random

from .payload import PandasFrameData
from .payload.payload import build_payload
from .queue import get_queue

from .collector_base import CollectorBase
from .context import CorrelationContext, get_context

try:
    import pandas as pd
except ImportError:
    pass


def _build_log_data_by_type(data):
    if 'pandas' in sys.modules and isinstance(data, pd.DataFrame):
        return PandasFrameData(data)

    raise TypeError("data type (%s) not supported, "
                    "supported types: pandas.DataFrame"
                    % type(data).__name__)


class JsonCollector(CollectorBase):
    def __init__(
            self,
            *,
            name: str,
            column_names: list = None
    ):
        super().__init__("default")
        self.name = name
        self.column_names = column_names

    def collect(
            self,
            data,  # supported type: Union[pd.DataFrame]
            correlation_context: CorrelationContext = None) -> CorrelationContext:
        if correlation_context is None:
            correlation_context = get_context()

        config = self.config
        if config is None:
            return self._response(correlation_context, False, "data collector is not initialized")

        if not config.enabled():
            self.logger.debug("data collector is not enabled, drop the data")
            return self._response(correlation_context, True, "dropped")

        # apply sampling on client side
        sample_rate = config.sample_rate()
        if sample_rate < 100:
            if sample_rate <= random.random() * 100.0:
                self.logger.debug("sampling not hit, drop the data")
                # TBD: send empty message to mdc to collect metrics of dropped messages?
                return self._response(correlation_context, True, "dropped_sampling")

        try:
            # build payload and put into payload queue
            logdata = _build_log_data_by_type(data)
            payload = build_payload(
                self.name,
                data=logdata,
                model_version=config.model_version(),
                context=correlation_context)

            success, msg = get_queue().enqueue(payload)
            return self._response(correlation_context, success, msg)
        except TypeError as e:
            return self._response(correlation_context, False, e.args[0])
