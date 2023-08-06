import dataclasses
from typing import Type, Any


@dataclasses.dataclass
class ProtocolConfig:
    sender: str = "sender"
    recipient: str = "recipient"
    serializer: str = "json"


@dataclasses.dataclass
class SubscriberConfig:
    prefetch_count: int = 1
    accept: str = "application/json"


@dataclasses.dataclass
class Config:
    queue: str = "MargayGatewayDefaultConsumer"
    dsn: str = "amqp://user:bitnami@localhost:5672/"
    inbox: str = "MargayGatewayInbox"
    outbox: str = "MargayGatewayOutbox"
    protocol: Type[ProtocolConfig] = ProtocolConfig
    subscriber: Type[SubscriberConfig] = SubscriberConfig

    @classmethod
    def from_env(cls):
        raise NotImplementedError

    @classmethod
    def from_object(cls):
        raise NotImplementedError

    @classmethod
    def from_dict(cls, conf: dict):
        raise NotImplementedError

    @classmethod
    def set(cls, key: str, value: Any):
        getattr(cls, key)
        setattr(cls, key, value)
