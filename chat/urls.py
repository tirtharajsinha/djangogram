from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat_index, name="chat-index"),
    path("login", views.loginView, name="login"),
    path("register", views.registerView, name="register"),
    path("logout", views.logoutView, name="register"),
    path("newroom", views.create_room, name="chat-create-room"),
    path("<str:room_uuid>/", views.room_view, name="chat-room"),
    path(
        "privatechat/<str:privateuser>",
        views.create_private_chat_room,
        name="chat-create-private",
    ),
    path("getchatsearch/<str:query>", views.get_search_data, name="chat-search"),
    path("inviteuser", views.invite_user_to_group, name="user-invite"),
]
