# Generated by Django 4.2.10 on 2024-02-15 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0003_card_description_card_image_card_status_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="card",
            old_name="status",
            new_name="status_url",
        ),
        migrations.AlterField(
            model_name="card",
            name="status_code",
            field=models.CharField(default="200", max_length=4),
        ),
        migrations.AlterField(
            model_name="group",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
