import json
import logging
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_not_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.html import escape
from django.views import View
from ping3 import ping

from . import CardCreationException
from .card_form import CardForm
from .config_yml import read_config_yml, write_config_yml
from .models import Card, Card_name_max_length, Group, Group_name_max_length, UserSettings
from .utils import _get_edit_mode, _get_icon_form_table, _get_image_list

MAX_SIZE_IMAGE_LIST = 10
MAX_SIZE_START_TIME = 100
START_TIME = [datetime.now()] * MAX_SIZE_START_TIME


class AjaxIconAutoComplete(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "partials/images.html",
            {
                "images": _get_image_list(request.GET["image"]),
                "icon_form_table": _get_icon_form_table(request),
            },
        )


class AjaxIconFormTableMenu(View):
    def get(self, request, *args, **kwargs):
        # just to show how to handle the endpoint a class
        if request.user.is_authenticated:
            new_user_settings = UserSettings.objects.get(user=request.user)
            new_user_settings.icon_form_table = not new_user_settings.icon_form_table
            new_user_settings.save(update_fields=["icon_form_table"])
        return render(
            request,
            "partials/icon_form_table.html",
            {
                "icon_form_table": _get_icon_form_table(request),
            },
        )


def edit_mode_menu(request):
    if request.user.is_authenticated:
        new_user_settings = UserSettings.objects.get(user=request.user)
        new_user_settings.edit_mode = not new_user_settings.edit_mode
        new_user_settings.save(update_fields=["edit_mode"])
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
    }
    return render(request, "partials/dashboard.html", context)


@login_not_required
def index(request):
    read_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
        "icon_form_table": _get_icon_form_table(request),
    }
    return render(request, "partials/dashboard.html", context)


def card_list(request):
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
    }
    return render(request, "partials/groups.html", context)


def card_create(request, group_name):
    req_name = escape(request.GET["q"])
    req_name = req_name[: Card_name_max_length - 1]
    name = Card.objects.filter(name=req_name).first()
    group = Group.objects.get(name=group_name)
    if not name and req_name and group:
        card = Card(name=req_name, group=group)
        card.save()
        write_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
    }
    return render(request, "partials/groups.html", context)


def card_delete(request, card_id):
    instance = Card.objects.get(id=card_id)
    if instance:
        instance.delete()
    write_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
    }
    return render(request, "partials/groups.html", context)


def card_edit_popup(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            try:
                newObject = form.save()
                write_config_yml()
            except Exception as error:  # forms.ValidationError
                raise CardCreationException(str(form.cleaned_data) + str(newObject))
            if newObject:
                return HttpResponse(
                    f"Card {card.name} updated.",
                    status=201,
                    headers={
                        "HX-Trigger": json.dumps({"cardListChanged": None, "showMessage": f"{card.name} updated."})
                    },
                )
    else:
        form = CardForm(instance=card)
    return render(
        request,
        "partials/card_edit_popup.html",
        {
            "form": form.initial,
            "icon_form_table": _get_icon_form_table(request),
        },
    )


def card_status(request, card_id):
    card_id = int(card_id)
    card = get_object_or_404(Card, pk=card_id)
    if ":" not in card.url:
        status = ping(card.status_url)
    else:
        try:
            response = requests.get(card.url, verify=False, timeout=60)
            status = response.elapsed.total_seconds()
            if card_id < MAX_SIZE_START_TIME:
                START_TIME[card_id] = datetime.now()
        except requests.ConnectionError as e:
            # expected exception, when the service to check go down
            if card_id < MAX_SIZE_START_TIME:
                status = (datetime.now() - START_TIME[card_id]).seconds
            else:
                status = (datetime.now() - START_TIME[-1]).seconds
        except Exception as e:
            # todo: must be managed before deploy in prod
            logging.critical("Unexpected Exception, do you try to break the server ?")
    return render(
        request,
        "partials/card_status.html",
        {
            "status": status,
        },
    )


def group_create(request):
    req_name = escape(request.GET["q"])
    req_name = req_name[: Group_name_max_length - 1]
    name = Group.objects.filter(name=req_name).fist()
    if not name and req_name:
        group = Group(name=req_name)
        group.save()
        write_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
    }
    return render(request, "partials/groups.html", context)


def group_delete(request, group_id):
    instance = Group.objects.get(id=group_id)
    if instance:
        # The delete cascade will delete all card in that group
        instance.delete()
    write_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {
        "groups": groups,
        "cards": cards,
        "edit_mode": _get_edit_mode(request),
    }
    return render(request, "partials/groups.html", context)
