from django.shortcuts import render
from chat.models import Room, Message
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.db.models import Q


def index_view(request):
    user = request.user
    rooms = Room.objects.filter(
        Q(type="group") | (Q(firstUser=user) | Q(secondUser=user))
    )
    return render(
        request,
        "index.html",
        {
            "rooms": rooms,
        },
    )


def room_view(request, room_name):
    if "__" in room_name:
        return HttpResponseNotFound("Chat not found")

    PrivateChat = User.objects.filter(username=room_name).first()
    user = request.user
    if PrivateChat != None:
        if PrivateChat.username == user.username:
            return HttpResponseNotFound("Invalid Chat")

        chatUserList = [user.username, PrivateChat.username]
        chatUserList.sort()

        room_name = "__".join(chatUserList)

        chat_room, created = Room.objects.get_or_create(
            name=room_name,
            defaults={"type": "private", "firstUser": user, "secondUser": PrivateChat},
        )
    else:
        chat_room, created = Room.objects.get_or_create(name=room_name)
    room_messages = Message.objects.filter(room=chat_room)
    rooms = Room.objects.filter(
        Q(type="group") | (Q(firstUser=user) | Q(secondUser=user))
    )

    print(rooms)
    return render(
        request,
        "room.html",
        {"room": chat_room, "room_messages": room_messages, "rooms": rooms},
    )


def private_view(request, recipient):
    pass
