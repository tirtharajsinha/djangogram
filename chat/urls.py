from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat_index, name="chat-index"),
    path("newroom", views.create_room, name="chat-create-room"),
    path("<str:room_uuid>/", views.room_view, name="chat-room"),
    path(
        "privatechat/<str:privateuser>",
        views.create_private_chat_room,
        name="chat-create-private",
    ),
    path("getchatsearch/<str:query>", views.get_search_data, name="chat-search"),
]
