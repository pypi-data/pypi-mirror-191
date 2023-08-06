from typing import Type

from kombu import Exchange, Queue, Connection
from kombu.mixins import ConsumerMixin

from margay.sdk.config import Config
from margay.sdk.logger import SDKLogger
from margay.sdk.protocol import BaseMessage, RawMessage


class Subscriber(ConsumerMixin):
    conf: Type[Config] = Config
    Message: Type[BaseMessage] = RawMessage

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=[self.queue],
                on_message=self.on_message,
                accept={self.conf.subscriber.accept},
                prefetch_count=self.conf.subscriber.prefetch_count,
            )
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SDKLogger.debug(f"Creating connection to `{self.conf.dsn}`")
        self.connection = Connection(self.conf.dsn)
        SDKLogger.debug(f"Setup exchange to `{self.conf.outbox}`")
        self.exchange = Exchange(self.conf.outbox, "topic", durable=True)
        SDKLogger.debug(f"Bind queue `{self.conf.queue}` to exchange `{self.conf.outbox}`")
        self.queue = Queue(self.conf.queue, exchange=self.exchange)

    def on_message(self, entry):
        SDKLogger.debug(f"Received RAW message, body: `{entry.body}`, headers:`{entry.headers}`")
        try:
            message = self.Message.from_transport(entry)
        except self.Message.InvalidMessage as err:
            SDKLogger.warning(f"Can't decode message - {err}")
            self.on_decode_error(entry, err)
            return

        SDKLogger.debug(f"Message `{message.id}` was successfully decoded")

        try:
            self.process(message)
        except Exception as err:
            SDKLogger.error(f"Fail while processing message `{message.id}` - {err}")
            self.on_fail(message, entry, err)
        else:
            SDKLogger.debug(f"Message `{message.id}` was successfully processed")
            self.on_success(message, entry)

    def process(self, message: BaseMessage):
        SDKLogger.info(f"Processing message `{message.id}` - {message}")

    def on_success(self, message: BaseMessage, entry):
        self.finalize(message, entry)

    def on_fail(self, message: BaseMessage, entry, exc: Exception):
        self.finalize(message, entry)

    @staticmethod
    def finalize(message: BaseMessage, entry):
        entry.ack()
        SDKLogger.debug(f"Message `{message.id}` has been acknowledged")
