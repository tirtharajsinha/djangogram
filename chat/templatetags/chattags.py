from django import template
from django.core.serializers import serialize
import json, re

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


@register.filter
def querysetToJson(queryset):
    return list(queryset.values())


@register.filter
def filterMsg(value):
    # Replace url to link
    urls = re.compile(
        r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)",
        re.MULTILINE | re.UNICODE,
    )
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    # Replace email to mailto
    urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE | re.UNICODE)
    value = urls.sub(r'<a href="mailto:\1" target="_blank">\1</a>', value)

    matches = list(filter(lambda word: word[0] == "@", value.split()))
    # print(matches)
    for match in matches:
        val = match[1:]
        value = value.replace(
            match, f"<a href='/chat/privatechat/{val}' class='tagtype'>{match}</a>"
        )

    # print(value, flush=True)
    return value


@register.filter
def isAuthtypeChecker(authtype, value):
    if authtype == value:
        return "openform"
    else:
        return ""


@register.filter
def enableRegisterForm(authtype, subvalue):
    if authtype == "register":
        return f"{subvalue}-toggle"
