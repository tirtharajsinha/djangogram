from django.contrib import admin

from chat.models import Room, Message, LetestMessage, JoinedRoom

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(LetestMessage)
admin.site.register(JoinedRoom)
