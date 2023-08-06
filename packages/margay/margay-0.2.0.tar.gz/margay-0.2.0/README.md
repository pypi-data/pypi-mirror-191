# Margay Gateway - toolkit
Provide set of tooling for building reliable websocket gateway system. 
Architecture part described in Margay Gateway core [repository](https://github.com/moaddib666/wss-api-gateway.go#readme)

## Quickstart

- Install sdk `pip install margay`
- Deploy `Margay Gateway` with RMQ locally part see [instruction](https://github.com/moaddib666/wss-api-gateway.go#local-stand)
- Setup Subscriber or use example `examples/vanilla_worker.py` or `examples/vanilla_publisher.py` 
- Setup client or use example `examples/vanilla_client.py`
  - You can generate auth token by using [cli](https://github.com/moaddib666/wss-api-gateway.go/blob/main/cmd/indentety_provider/encoder.go)
  - By using sdk auth
  - By using external indentety provider
- Connect your backend
  - Basically that means:
    - You subscribe RMQ topic with your `CustomQueue` and listen for events
    - You are ready to publish new events for your clients
- Connect websocket client to `Margay Gateway`
- That's it now you are ready to send/receive messages trough `Margay Gateway`

## Configure
You are able to setup sdk for your custom needs

Example of change of default subscriber queue name
```python
from margay.sdk.config import Config

Config.set("queue", "VanillaWorkerQueue")
```

## Subscriber
Example custom subscriber creation 
```python
from margay.sdk.subscriber import Subscriber
from margay.sdk.protocol import RawMessage

class JsonMessage(RawMessage):
    """ Your message protocol """

class Router:
    """ Your event router """

class Handler:
    """ Your event handler """
    
class SimpleWorker(Subscriber):
    Message = JsonMessage
    resolve = Router.resolve
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self, message: JsonMessage):
        self.resolve(message)

```

## Publisher
Example custom publisher creation

```python
from margay.sdk.publisher import Publisher

class Event:
    """Your custom event protocol"""
    
class EventPublisher(Publisher):
    origin = "MyAwsomeMss"
    def publish(self, event: Event, recipient: str):
        self.publish_raw(event.serialize(), self.origin, recipient)
```

## Auth
### JWT
```python
from margay.sdk.auth import JWTAuth
user = "John Snow"
secret = "SuperSecret"
identity_provider = JWTAuth(secret)
token = identity_provider.issue_token(user)
payload = identity_provider.verify_token(token, user)
print(payload)
```

## Debugging
Set debug for SDKLogger
```python
import logging
from margay.sdk.logger import SDKLogger
import sys
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
SDKLogger.setLevel(logging.DEBUG)
```
