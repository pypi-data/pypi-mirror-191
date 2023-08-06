from typing import Dict, List

from rudder_analytics import client
from apna_python_experiment_sdk.base import Configuration, SinkSerializer, Sink
import logging
from mixpanel import Mixpanel
from apna_python_experiment_sdk.custom.mixpanel.async_mixpanel_buffered_consumer import AsyncBufferedConsumer
from .mixpanel_sink import MixpanelExperimentConfiguration, MixpanelExperimentSerializer
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit


class AsyncMixpanelExperimentSink(Sink):
    client = None

    def __init__(self, configuration: Configuration = MixpanelExperimentConfiguration, serializer: SinkSerializer = MixpanelExperimentSerializer):
        super().__init__(configuration, serializer)

        if client is not None:
            # Initialize conf and serializer:
            self.configuration = configuration()
            self.serializer = serializer()

            # Initialze mixpanel client:
            conf = self.configuration.get_conf()

            # Creating custom buffered consumer:
            custom_buffered_consumer = AsyncBufferedConsumer(
                buffer_size=conf['buffer_size'], max_size=conf['max_flush_size'])

            self.client = Mixpanel(
                conf['api_token'], consumer=custom_buffered_consumer)

            self.scheduler = BackgroundScheduler()
            self.flush_job: Job = None
            self.scheduler.start()
            self.flush_job = self.scheduler.add_job(self.flush,
                                                    trigger=IntervalTrigger(
                                                        seconds=conf['flush_interval']))
            logging.info(
                f'MixpanelExperimentSink initialzed with batch size: {custom_buffered_consumer._max_size}')
            atexit.register(self.__close)
        else:
            logging.warning('MixpanelExperimentSink is already initialized!')

    def __close(self):
        logging.warning(
            f'AsyncMixpanelSink destructor called. Now flushing the events.')
        self.flush()
        if self.flush_job:
            self.flush_job.remove()
        self.scheduler.shutdown()

    def flush(self):
        self.client._consumer._join_flush_thread()
        num_events = len(self.client._consumer._async_buffers["imports"])
        if num_events > 0:
            logging.warning(
                f'Flushing {num_events} events in the buffer to mixpanel.')
            self.client._consumer.flush(asynchronous=False)
            logging.warning(f'Flushed.')
        else:
            logging.info(f'No events was there to flush in AsyncMixpanelSink.')
            return

    def push(self, element: dict, **kwargs) -> bool:
        """This method calls the import_data method of the mixpanel client to send around 2000 events per API
        call.

        Args:
            element (dict): The variant and user_id fetched from experiment_client.

        Returns:
            bool: Returns true if success.
        """

        serialized_data = self.serializer.serialize(element=element, **kwargs)
        conf = self.configuration.get_conf()

        try:
            self.client.import_data(
                api_key=conf['api_token'],
                api_secret=conf['project_secret'],
                **serialized_data)
        except Exception as e:
            logging.warning(
                f'Error while pushing data into AsyncMixpanelExperimentSink: {e}')
        return True

    def bulk_push(self, serialized_elements: List[dict]) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in AsyncMixpanelExperimentSink.')

    def trigger(self):
        raise NotImplementedError(
            f'This function is not implemented and not required in AsyncMixpanelExperimentSink.')

    def trigger_condition(self) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in AsyncMixpanelExperimentSink.')
