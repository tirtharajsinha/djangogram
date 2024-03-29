# Generated by Django 4.0 on 2024-02-19 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.CharField(choices=[('group', 'group'), ('private', 'private')], default='group', max_length=128),
        ),
        migrations.CreateModel(
            name='LetestMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.message')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.room')),
            ],
        ),
    ]
