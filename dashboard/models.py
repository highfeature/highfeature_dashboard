from django.db import models

from highfeature_dashboard.users.models import User

Group_name_max_length = 200


class Group(models.Model):
    name = models.CharField(max_length=Group_name_max_length, unique=True)


Card_name_max_length = 22
Card_desc_max_length = 100
Card_image_max_length = 100
Card_url_max_length = 150
Card_status_max_length = 150
Card_status_freq_min = 3
Card_status_freq_max = 60 * 60 * 24
Card_code_max_length = 4
Card_docker_container_name_max_length = 128
Card_docker_env_max_length = 2


class Card(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=Card_name_max_length)
    description = models.CharField(max_length=Card_desc_max_length, default="")
    image = models.CharField(max_length=Card_image_max_length, default="arch-linux.png")
    url = models.URLField(max_length=Card_url_max_length, default="")
    # Status
    status_enable = models.BooleanField(default=False)
    status_url = models.URLField(max_length=Card_status_max_length, default="")
    status_code = models.CharField(max_length=Card_code_max_length, default="200")
    status_freq = models.IntegerField(default=10)
    # Docker
    docker_server_url = models.URLField(max_length=Card_url_max_length, default="")
    docker_env = models.CharField(max_length=Card_docker_env_max_length, default="1")
    docker_container_name = models.CharField(max_length=Card_docker_container_name_max_length, default="")
    docker_container_status = models.CharField(max_length=Card_docker_container_name_max_length, default="")
    docker_container_uptime = models.CharField(max_length=Card_docker_container_name_max_length, default="")


class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edit_mode = models.BooleanField(default=False)
    # user preference
    icon_form_table = models.BooleanField(default=False)


class Notification(models.Model):
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "created:" + str(self.created) + " message:" + self.message
