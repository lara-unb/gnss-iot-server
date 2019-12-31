import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.db import database_sync_to_async
from gnss_iot_server.sock_data import create_connection, get_data

import time
import selectors


ids = ["3236D37B277EC67E4C49929986AC6CED"]

class GnssConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connected", event)
        self.send({
            "type": "websocket.accept"
        })
        
        sel = selectors.DefaultSelector()
        create_connection(ids, sel)

        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data != None:
                    data = get_data(key, mask, sel)
                    if data != None:
                        self.send({
                            "type": "websocket.send",
                            "text": json.dumps(data),
                        })
                    else:
                        break

    def websocket_receive(self, event):
        print("receive", event)

    def websocket_disconnect(self, event):
        print("disconnect", event)
        # sel.unregister(sock)
        # close(sock)
