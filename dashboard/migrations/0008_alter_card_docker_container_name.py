# Generated by Django 4.2.10 on 2024-02-17 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0007_card_docker_env"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="docker_container_name",
            field=models.CharField(default="", max_length=128),
        ),
    ]
