from django import template

register = template.Library()


# input : user1:current_user | output: user1
@register.filter
def room_to_private(room, user):
    # print(room.name,, roomName)
    roomname = room.name
    roomtype = room.type
    currentuser = user.username
    try:
        if roomtype == "private":
            result = roomname.split("__")
            result.remove(currentuser)
            return result[0]
        return roomname
    except:
        raise Exception(f"{roomname} {roomtype} {currentuser}")
