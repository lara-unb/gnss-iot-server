import asyncio
import json
from django.contrib.auth import  get_user_model
from channels.consumer import  AsyncConsumer
from channels.db import database_sync_to_async
from gnss_iot_server import pybinn
from gnss_iot_server.settings import sock
from .sock_data import get_data


class GnssConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type":"websocket.accept"
        })

        
        while True:
            data = get_data()
            
            await  self.send({
                "type":"websocket.send",
                "text": json.dumps(data),
            })
            await  asyncio.sleep(1)

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnect", event)
