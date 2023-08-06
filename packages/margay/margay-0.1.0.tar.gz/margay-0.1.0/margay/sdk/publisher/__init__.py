from typing import Type
from kombu import Producer, Connection, Exchange
from margay.sdk.config import Config
from margay.sdk.logger import SDKLogger


class Publisher:

    conf: Type[Config] = Config

    def __init__(self):
        SDKLogger.debug(f"Creating connection to `{self.conf.dsn}`")
        self.connection = Connection(self.conf.dsn)
        SDKLogger.debug(f"Setup exchange to `{self.conf.inbox}`")
        self.exchange = Exchange(self.conf.inbox, "direct")
        self.connection.connect()

    def publish_raw(self, msg: str, sender: str, recipient: str):
        with self.connection.channel() as channel:
            SDKLogger.debug(f"Setup producer with {self.exchange} serialized by `{self.conf.protocol.serializer}`")
            producer = Producer(
                channel, serializer=self.conf.protocol.serializer, exchange=self.exchange, auto_declare=True
            )
            headers = {
                    self.conf.protocol.sender: sender,
                    self.conf.protocol.recipient: recipient,
                }
            SDKLogger.debug(f"Publishing RAW message body:`{msg}`, headers: `{headers}`")
            producer.publish(
                msg,
                retry=True,
                headers=headers,
            )

    def __del__(self):
        SDKLogger.debug(f"Close connection to `{self.connection}`")
        self.connection.close()
