import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        # Get the message
        message = event["message"]

        # follow process Django do for normal view
        template = Template('<div id="notification"><p>{{message}}</p></div>')
        context = Context({"message": message})
        rendered_notification = template.render(context)
        await self.send(text_data=json.dumps({"type": "notification", "message": rendered_notification}))
