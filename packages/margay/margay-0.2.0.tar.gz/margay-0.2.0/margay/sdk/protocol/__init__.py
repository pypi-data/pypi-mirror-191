import abc
import uuid

from pydantic import BaseModel, Field


class BaseMessage(BaseModel):

    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    @classmethod
    @abc.abstractmethod
    def from_transport(cls, message) -> "BaseMessage":
        pass

    @abc.abstractmethod
    def event_name(self) -> str:
        pass

    class InvalidMessage(Exception):
        pass


class RawMessage(BaseMessage):

    body: str
    headers: dict

    def event_name(self) -> str:
        return "rawMessage"

    @classmethod
    def from_transport(cls, message) -> "BaseMessage":
        try:
            return cls.construct(message)
        except Exception as err:
            raise cls.InvalidMessage(f"Can't construct {cls} from message") from err

    @classmethod
    def construct(cls, message) -> "BaseMessage":
        return cls(body=message.body, headers=message.headers)
