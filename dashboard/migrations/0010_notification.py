# Generated by Django 4.2.10 on 2024-02-19 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0009_alter_card_docker_container_status_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
