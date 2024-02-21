from django.contrib.auth.models import User
from django.db import models
import uuid


TYPE_OF_ROOMS_CHOICES = [("group", "group"), ("private", "private")]


class Room(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)
    type = models.CharField(
        max_length=128, choices=TYPE_OF_ROOMS_CHOICES, default="group"
    )

    admin = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="room_admin",
    )

    firstUser = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="room_first_user",
    )

    secondUser = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        related_name="room_second_user",
    )

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp.strftime("%I:%M%p %d %b, %Y")}]'


class LetestMessage(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)


class JoinedRoom(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)
