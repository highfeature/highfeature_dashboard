from django import forms

from .models import (
    Card,
    Card_code_max_length,
    Card_desc_max_length,
    Card_docker_container_name_max_length,
    Card_docker_env_max_length,
    Card_image_max_length,
    Card_name_max_length,
    Card_status_max_length,
    Card_url_max_length,
)
from .utils import _get_image_list


# TODO: fix translation
def _(s):
    return s


class CardForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=Card_name_max_length, label=_("Name"))
    description = forms.CharField(required=False, max_length=Card_desc_max_length, label=_("Description"))
    image = forms.CharField(
        required=False, max_length=Card_image_max_length, initial="arch-linux.png", label=_("Image")
    )
    url = forms.URLField(required=True, max_length=Card_url_max_length, initial="", label=_("Url"))
    status_enable = forms.BooleanField(required=False, initial=False, label=_("Enable Status"))
    status_url = forms.URLField(required=False, max_length=Card_status_max_length, initial="", label=_("Status Url"))
    status_code = forms.CharField(
        required=False, max_length=Card_code_max_length, initial="200", label=_("Status Code")
    )
    status_freq = forms.IntegerField(
        required=False, min_value=3, max_value=60 * 60 * 24, initial="10", label=_("Freq. Check in seconds (min 3)")
    )
    docker_server_url = forms.URLField(
        required=False, max_length=Card_url_max_length, initial="", label=_("Docker Server URL")
    )
    docker_env = forms.CharField(
        required=False, max_length=Card_docker_env_max_length, initial="1", label=_("Docker Env")
    )
    docker_container_name = forms.CharField(
        required=False, max_length=Card_docker_container_name_max_length, initial="", label=_("Docker Container Name")
    )

    class Meta:
        model = Card
        # exclude = ['docker_container_status','docker_container_uptime']
        fields = [
            "name",
            "description",
            "image",
            "url",
            "status_enable",
            "status_url",
            "status_code",
            "status_freq",
            "docker_server_url",
            "docker_env",
            "docker_container_name",
        ]

    def clean_image(self):
        items = _get_image_list(self.cleaned_data.get("image"))
        image = items[0] if len(items) else ""
        return image
