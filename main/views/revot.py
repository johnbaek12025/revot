from dummy_data import random_date
from datetime import datetime
import random
import requests
import websocket
import json


main_url = 'https://revot.ai/'
ses = requests.session()

class BringContents:
    def __init__(self, msg) -> None:
        self.response = []
        self.msg = msg        
        
    def on_message(self, ws, message):
        # Decode the message using json.loads()
        data = json.loads(message)
        # Close the WebSocket connection
        ws.close()
        self.response.append(data)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws):
        print("WebSocket closed")

    def on_open(self, ws):
        print("WebSocket opened")
        # Send a message over the WebSocket connection        
        ws.send(json.dumps(self.msg))
        
    def main(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://revot.ai/ws/fetch/contents/",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()
        return self.response[0]