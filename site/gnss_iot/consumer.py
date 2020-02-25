import time
import json
import asyncio
import selectors
from .models import Device
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer, SyncConsumer
from gnss_iot_server.sock_data import create_connection, get_data


class GnssConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connected", event)
        self.send({
            "type": "websocket.accept"
        })
        self.sel = selectors.DefaultSelector()
        devices = get_device(self.scope["user"])
        self.ids = []
        self.devices_id = []
        self.devices_list = []
        for device in devices:
            self.ids.append(device.token)
        create_connection(self.ids, self.sel)

    def websocket_receive(self, event):

        events = self.sel.select(timeout=None)
        for self.key, self.mask in events:
            if self.key.data != None:
                data = get_data(self.key, self.mask, self.sel)
                if data is not None:
                    if data['id'] not in self.devices_id:
                        devices = get_device(self.scope["user"])
                        for device in devices:
                            if device.token == data['id']:
                                data['name'] = device.name
                        self.devices_list.append(data)
                        self.devices_id.append(data['id'])

                    else:
                        for i in self.devices_list:
                            if i['id'] == data['id']:
                                i['coord'][0] = data['coord'][0]
                                i['coord'][1] = data['coord'][1]
                    print(data)
                    print(self.devices_list)

                    self.send({
                        "type": "websocket.send",
                        "text": json.dumps(self.devices_list),
                    })

    def websocket_disconnect(self, event):
        self.ids = []
        self.devices_id = []
        self.devices_list = []
        print("disconnect", event)
        self.sel.unregister(self.key.fileobj)
        self.key.fileobj.close()
        self.sel.close()


def get_device(user):
    devices = Device.objects.filter(owner=user)
    return devices


def get_device_id(device_id):
    device = Device.objects.filter(id=device_id)
    return device
