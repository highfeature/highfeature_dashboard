# Generated by Django 4.2.10 on 2024-02-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0002_usersettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="description",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="card",
            name="image",
            field=models.CharField(default="dashboard_icons/png/arch.png", max_length=100),
        ),
        migrations.AddField(
            model_name="card",
            name="status",
            field=models.URLField(default="", max_length=150),
        ),
        migrations.AddField(
            model_name="card",
            name="status_code",
            field=models.CharField(default="200", max_length=3),
        ),
        migrations.AddField(
            model_name="card",
            name="status_enable",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="card",
            name="url",
            field=models.URLField(default="", max_length=150),
        ),
        migrations.AlterField(
            model_name="card",
            name="name",
            field=models.CharField(max_length=30),
        ),
    ]
