import websocket
from margay.sdk.logger import SDKLogger


class Client:
    def __init__(self, dsn: str, token: str):
        self.opened = False
        self.ws = websocket.create_connection(
            dsn,
            header={
                 'Authorization': f'Bearer {token}'
            },
        )

    def send_message(self, msg: str):
        self.ws.send(msg.encode())

    def get_message(self) -> str:
        return self.ws.recv().decode()

    def run(self):
        while True:
            message = input("Send to WSS: ")
            if message:
                SDKLogger.debug(f"Sending to {self.ws}")
                print(f" -> {message}")
                self.send_message(message)
            respond = self.get_message()
            print(f" <- {respond}")
            SDKLogger.debug(f"Connection respond with {respond}")
