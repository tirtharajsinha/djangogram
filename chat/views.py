import json
from django.forms import ValidationError, model_to_dict
from django.shortcuts import render, redirect
from chat.models import Room, Message, JoinedRoom
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def chat_index(request):
    user = request.user
    joined_rooms = JoinedRoom.objects.filter(user=user).values_list("room")
    rooms = Room.objects.filter(
        Q(id__in=joined_rooms) | Q(firstUser=user) | Q(secondUser=user) | Q(admin=user)
    ).order_by("-id")

    # print(list(joined_rooms), list(rooms), flush=True)
    return render(
        request,
        "index.html",
        {
            "rooms": rooms,
        },
    )


@login_required
def create_room(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body)
            room_name = json_data.get("room_name")
            if room_name == None:
                return JsonResponse({"error": "room_name required"})
            elif room_name == "":
                return JsonResponse({"error": "room_name required"})
            elif "__" in room_name:
                return JsonResponse({"error": "__ not allowed"})
            elif len(room_name) < 5:
                return JsonResponse({"error": "room_name must have 5 characters"})
            elif "#" in room_name:
                return JsonResponse({"error": "# is not allowed"})

            usermatch = User.objects.filter(username=room_name).first()
            if usermatch:
                return JsonResponse({"error": "Invalid room name"})

            chat_room = Room.objects.filter(name=room_name).first()
            if chat_room:
                return JsonResponse({"error": "room already exists"})
            else:
                newroom = Room.objects.create(name=room_name, admin=request.user)
                joinroom = JoinedRoom.objects.create(room=newroom, user=request.user)
                return JsonResponse(
                    {
                        "success": "room created successfully",
                        "newroom_unique_id": newroom.unique_id,
                    }
                )
        except Exception as e:
            return JsonResponse({"error": "Something went wrong", "statement": str(e)})
    return redirect("/chat")


@login_required
def room_view(request, room_uuid):
    try:
        chat_room = Room.objects.filter(unique_id=room_uuid).first()
    except Exception as e:
        return redirect("/chat")

    if chat_room == None:
        return redirect("/chat")

    user = request.user
    if chat_room.type == "private":
        if chat_room.firstUser.id != user.id and chat_room.secondUser.id != user.id:
            return redirect("/chat")

    if chat_room.type == "group":
        joinroom = JoinedRoom.objects.get_or_create(room=chat_room, user=request.user)

    room_messages = Message.objects.filter(room=chat_room)

    joined_rooms = JoinedRoom.objects.filter(user=user).values_list("room")
    rooms = Room.objects.filter(
        Q(id__in=joined_rooms) | Q(firstUser=user) | Q(secondUser=user) | Q(admin=user)
    ).order_by("-id")

    print(rooms)
    return render(
        request,
        "room.html",
        {"room": chat_room, "room_messages": room_messages, "rooms": rooms},
    )


@login_required
def create_private_chat_room(request, privateuser):
    PrivateChat = User.objects.filter(username=privateuser).first()

    user = request.user
    if privateuser == None:
        return redirect("/chat")
    else:
        if PrivateChat.username == user.username:
            return redirect("/chat")

        chatUserList = [user.username, PrivateChat.username]
        chatUserList.sort()

        room_name = "__".join(chatUserList)

        chat_room, created = Room.objects.get_or_create(
            name=room_name,
            defaults={"type": "private", "firstUser": user, "secondUser": PrivateChat},
        )

        return redirect(f"/chat/{chat_room.unique_id}")


@login_required
def get_search_data(request, query):
    rooms = Room.objects.values("unique_id", "name", "type", "admin").filter(
        Q(type="group") & Q(name__icontains=query)
    )

    users = User.objects.filter(
        ~Q(username=request.user.username) & Q(username__icontains=query)
    ).values("username")
    print(list(users), flush=True)
    return JsonResponse({"rooms": list(rooms), "users": list(users)})
