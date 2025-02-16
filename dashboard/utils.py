import json
import os

from django.conf import settings

from dashboard.models import UserSettings

MAX_SIZE_IMAGE_LIST = 10


def _get_image_list(startswith: str, max_size: int = MAX_SIZE_IMAGE_LIST):
    # Path to the tree.json file
    tree_json_path = os.path.join(settings.BASE_DIR, "highfeature_dashboard", "static", "dashboard_icons", "tree.json")
    # Load the JSON data
    with open(tree_json_path, encoding="utf-8") as file:
        data = json.load(file)
    # Extract the relevant images
    images = []
    for item in data["png"]:
        if item.startswith(startswith):
            images.append(item)
        if len(images) > max_size:
            break
    return images


def _get_edit_mode(request):
    user_settings = []
    if request.user.is_authenticated:
        user_settings = UserSettings.objects.filter(user=request.user)
    return user_settings[0].edit_mode if len(user_settings) else False


def _get_icon_form_table(request):
    user_settings = []
    if request.user.is_authenticated:
        user_settings = UserSettings.objects.filter(user=request.user)
    return user_settings[0].icon_form_table if len(user_settings) else False
