# import requests
import json
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required

# from django.forms import Form
from django.http import HttpResponse

# from django.conf import settings
from django.shortcuts import get_object_or_404, render

# from django.urls import reverse
from django.utils.html import escape
from ping3 import ping

from .card_form import CardForm
from .config_yml import read_config_yml, write_config_yml
from .models import Card, Card_name_max_length, Group, Group_name_max_length, UserSettings

# from celery.result import AsyncResult
# from celery_progress.backend import Progress


# from django_celery_beat.models import IntervalSchedule, PeriodicTask


# from .tasks import get_video_stats

MAX_SIZE_START_TIME = 100
START_TIME = [datetime.now()] * MAX_SIZE_START_TIME


def _get_edit_mode(request):
    #    read_config_yml()
    class LocalUserSettings:
        edit_mode = False

    user_settings = [
        LocalUserSettings(),
    ]
    if request.user.is_authenticated:
        user_settings = UserSettings.objects.filter(user=request.user)
    return user_settings[0].edit_mode if len(user_settings) else False


def index(request):
    read_config_yml()
    context = {"edit_mode": _get_edit_mode(request)}
    return render(request, "partials/dashboard.html", context)


def card_list(request):
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {"groups": groups, "cards": cards, "edit_mode": _get_edit_mode(request)}
    return render(request, "partials/groups.html", context)


# def channel_search(request):
#     query = request.GET['q']
#     url = f'https://www.googleapis.com/youtube/v3/search?q={query}&type=channel&part=snippet&key={settings.YOUTUBE_API_KEY}'
#     res = requests.get(url)
#
#     results = res.json()['items']
#     context = {'results': results}
#     return render(request, 'partials/channel_search_results.html', context)


@login_required
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
    context = {"groups": groups, "cards": cards, "edit_mode": _get_edit_mode(request)}
    return render(request, "partials/groups.html", context)


@login_required
def card_delete(request, card_id):
    instance = Card.objects.get(id=card_id)
    if instance:
        instance.delete()
    write_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {"groups": groups, "cards": cards, "edit_mode": _get_edit_mode(request)}
    return render(request, "partials/groups.html", context)


@login_required
def card_edit_popup(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            write_config_yml()
            return HttpResponse(
                status=201,
                headers={"HX-Trigger": json.dumps({"cardListChanged": None, "showMessage": f"{card.name} updated."})},
            )
    else:
        form = CardForm(instance=card)
    return render(
        request,
        "partials/card_edit_popup.html",
        {
            "form": form,
            "card": card,
        },
    )


@login_required
def card_status(request, card_id):
    card_id = int(card_id)
    card = get_object_or_404(Card, pk=card_id)
    # url = card.status_url
    if ":" not in card.url:
        status = ping(card.status_url)
    else:
        try:
            response = requests.get(card.url, verify=False, timeout=60)
            status = response.elapsed.total_seconds()
            if card_id < MAX_SIZE_START_TIME:
                START_TIME[card_id] = datetime.now()
        except Exception as e:
            if card_id < MAX_SIZE_START_TIME:
                status = (datetime.now() - START_TIME[card_id]).seconds
            else:
                status = (datetime.now() - START_TIME[-1]).seconds
    return render(
        request,
        "partials/card_status.html",
        {
            "status": status,
        },
    )


@login_required
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
    context = {"groups": groups, "cards": cards, "edit_mode": _get_edit_mode(request)}
    return render(request, "partials/groups.html", context)


@login_required
def group_delete(request, group_id):
    instance = Group.objects.get(id=group_id)
    if instance:
        # The delete cascade will delete all card in that group
        instance.delete()
    write_config_yml()
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {"groups": groups, "cards": cards, "edit_mode": _get_edit_mode(request)}
    return render(request, "partials/groups.html", context)


@login_required
def edit_mode_menu(request):
    class LocalUserSettings:
        edit_mode = False

    user_settings = [
        LocalUserSettings(),
    ]
    if request.user.is_authenticated:
        user_settings = new_user_settings = UserSettings.objects.get(user=request.user)
        new_user_settings.edit_mode = not new_user_settings.edit_mode
        new_user_settings.save(update_fields=["edit_mode"])
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")  # [0:50]
    context = {"groups": groups, "cards": cards, "edit_mode": user_settings.edit_mode}
    return render(request, "partials/dashboard.html", context)


# def generate(request):
#     task = get_video_stats.delay()
#     context = {'task_id': task.task_id, 'value': 0}
#     return render(request, 'partials/progress_bar.html', context)


# def get_next_rows(request):
#     offset = int(request.GET['offset'])
#     results = Video.objects.order_by('-views')[offset:offset+50]
#     context = {'results': results, 'offset': offset+50}
#     return render(request, 'partials/result_rows.html', context)


# @csrf_exempt
# def deletechannel(request, channel_id):
#     Channel.objects.filter(pk=channel_id).delete()
#
#     channels = Channel.objects.all()
#     context = {'channels': channels}
#     return render(request, 'partials/channels.html', context)


# def schedule_task(request):
#     interval, _ = IntervalSchedule.object.get_or_create(
#         every=1,
#         period=IntervalSchedule.HOURS,
#     )
#     PeriodicTask.object.create(
#         interval=interval,
#         name='my-schedule',
#         task='app.tasks.test_task',
#         #args=json.dumps(['arg1','arg2'],  # arg to pass to the task
#         #one_off=True,  # if you want run task only one time
#     )
#     return "Task Scheduled!"
