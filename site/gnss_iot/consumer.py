import asyncio
import json
from django.contrib.auth import  get_user_model
from channels.consumer import  AsyncConsumer,SyncConsumer
from channels.db import database_sync_to_async
from gnss_iot_server.sock_data import create_connection, get_data, FAILURE_SOCK

class GnssConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connected", event)
        self.send({
            "type":"websocket.accept"
        })

        sock = create_connection()
        if sock is not  FAILURE_SOCK:
            while True:
                data = get_data(sock)
                
                self.send({
                    "type":"websocket.send",
                    "text": json.dumps(data),
                })
            

    def websocket_receive(self, event):
        print("receive", event)

    def websocket_disconnect(self, event):
        print("disconnect", event)
