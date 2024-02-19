# Generated by Django 4.0 on 2024-02-19 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('chat', '0002_room_type_letestmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='firstUser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_first_user', to='auth.user'),
        ),
        migrations.AddField(
            model_name='room',
            name='secondUser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_second_user', to='auth.user'),
        ),
    ]
