from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import Conversation, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("room name is %s"%self.room_name)
        print("scope usr is %s"%str(self.scope['user']))
        self.room_group_name = 'chat_%s' % self.room_name
        
        #start of models logic
        self.users = self.room_name.split('-')

        #print(type(self.scope['user']))
        self.by_user = User.objects.get(username = self.scope['user'])
        for usr in self.users:
            print("for loop usr is %s"%usr)
            if usr != str(self.scope['user']):
                self.to_username = usr
        print("tousername is  %s"%self.to_username)

        self.to_user = User.objects.get(username = self.to_username)
        print(self.by_user)
        print(self.to_user)
        try:
            self.conv_object = Conversation.objects.get(started_by = self.by_user, sent_to = self.to_user)
        except:
            try:
                self.conv_object = Conversation.objects.get(started_by = self.to_user, sent_to = self.by_user)
            except:
                print(self.by_user)
                print(self.to_user)
                self.conv_object = Conversation(started_by = self.by_user, sent_to = self.to_user, chatroom = self.room_name)

                self.conv_object.save()

        #end of models logic



        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #print(self.scope['user'])

        #model logic
        #print(self.by_user.username)
        sender = User.objects.get(username = self.scope['user'])
        #print(sender)

        self.msg_object = Message(conv_id = self.conv_object, text = message,
                                 sender = User.objects.get(username = self.scope['user']),
                                 )
        self.msg_object.save()
        #end model logic


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sndr' : str(self.scope['user'])
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        messsage_user = event['sndr']


        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': messsage_user
        }))