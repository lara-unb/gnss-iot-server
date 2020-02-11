import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from gnss_iot_server.sock_data import create_connection, get_data

import time
import selectors


ids = ["3236D37B277EC67E4C49929986AC6CED", "47554EDEBB2DD0E304AE3C99D79D0471"]

class GnssConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connected", event)
        self.send({
            "type": "websocket.accept"
        })
        self.sel = selectors.DefaultSelector()
        create_connection(ids, self.sel)

    def websocket_receive(self, event):
        print("receive", event)
        
        events = self.sel.select(timeout=None)
        for self.key, self.mask in events:
            if self.key.data != None:
                data = get_data(self.key, self.mask, self.sel)
                if data is not None:
                    self.send({
                        "type": "websocket.send",
                        "text": json.dumps(data),
                    })
                else:
                    break

    def websocket_disconnect(self, event):
        print("disconnect", event)
        self.sel.unregister(self.key.fileobj)
        self.key.fileobj.close()
        self.sel.close()
