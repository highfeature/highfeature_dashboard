# Generated by Django 4.2.10 on 2024-02-17 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0008_alter_card_docker_container_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="docker_container_status",
            field=models.CharField(default="", max_length=128),
        ),
        migrations.AlterField(
            model_name="card",
            name="docker_container_uptime",
            field=models.CharField(default="", max_length=128),
        ),
    ]
