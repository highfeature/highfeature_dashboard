import yaml
from django.conf import settings
from django.db import transaction
from django.utils.html import escape

from dashboard.models import (
    Card,
    Card_code_max_length,
    Card_desc_max_length,
    Card_docker_container_name_max_length,
    Card_docker_env_max_length,
    Card_image_max_length,
    Card_name_max_length,
    Card_status_freq_max,
    Card_status_freq_min,
    Card_url_max_length,
    Group,
    Group_name_max_length,
)


def read_config_yml():
    Group.objects.all().delete()
    Card.objects.all().delete()
    fullname = settings.HF_DASHBOARD_CARDS_FILE
    with open(fullname) as file:
        configuration = yaml.safe_load(file)

    try:
        # Validate and sanitize
        # TODO: need add error msg in case of no respect of the rules
        for cg in configuration["groups"]:
            cg["name"] = escape(cg["name"][: Group_name_max_length - 1])
        for cc in configuration["cards"]:
            cc["group"] = escape(cc["group"][: Group_name_max_length - 1])
            cc["name"] = escape(cc["name"][: Card_name_max_length - 1])
            if "url" in cc:
                cc["url"] = cc["url"][: Card_url_max_length - 1]
            if "description" in cc:
                cc["description"] = escape(cc["description"][: Card_desc_max_length - 1])
            # TODO: Quick and dirty verif: explode that in multiple Django validator class
            if "image" in cc:
                cc["image"] = escape(cc["image"][: Card_image_max_length - 1])
                cc["image"] = (
                    cc["image"]
                    if cc["image"][0] not in ("/", ".")
                    and "//" not in cc["image"]
                    and "\\\\" not in cc["image"]
                    and ".." not in cc["image"]
                    else ""
                )
            # Status
            if "status_enable" in cc:
                cc["status_enable"] = cc["status_enable"] if cc["status_enable"] in (True, False) else True
                if "status_url" in cc:
                    cc["status_url"] = (
                        cc["status_url"]
                        if (
                            cc["status_url"][0] not in ("/", ".")
                            and "//" not in cc["status_url"]
                            and "\\\\" not in cc["status_url"]
                            and ".." not in cc["status_url"]
                        )
                        else ""
                    )
                if "status_code" in cc:
                    cc["status_code"] = cc["status_code"][: Card_code_max_length - 1]
                if "status_freq" in cc:
                    cc["status_freq"] = (
                        cc["status_freq"]
                        if Card_status_freq_max <= cc["status_freq"] <= Card_status_freq_min
                        else Card_status_freq_max
                    )
            # Docker
            if "docker_server_url" in cc:
                cc["docker_server_url"] = cc["url"][: Card_url_max_length - 1]
                if "docker_env" in cc:
                    cc["docker_env"] = cc["docker_env"][: Card_docker_env_max_length - 1]
                if "docker_container_name" in cc:
                    cc["docker_container_name"] = cc["docker_container_name"][
                        : Card_docker_container_name_max_length - 1
                    ]

        with transaction.atomic():
            groups = {}
            for _id, cg in enumerate(configuration["groups"]):
                group = Group(id=_id, name=cg["name"])
                group.save()
                groups[cg["name"]] = group
            for _id, cc in enumerate(configuration["cards"]):
                card = Card(
                    id=_id,
                    name=cc["name"],
                    group=groups[cc["group"]],
                )
                if "url" in cc and len(cc["url"]):
                    card.url = cc["url"]
                if "description" in cc and len(cc["description"]):
                    card.description = cc["description"]
                if cc["image"]:
                    card.image = cc["image"]
                if "status_url" in cc and cc["status_url"]:
                    card.status = cc["status_url"]
                if "status_code" in cc and cc["status_code"]:
                    card.status_code = cc["status_code"]
                if "status_enable" in cc and cc["status_enable"]:
                    card.status_enable = cc["status_enable"]
                card.save()
    except Exception as e:
        print(str(e))


def write_config_yml():
    groups = Group.objects.all()
    cards = Card.objects.order_by("-group")
    configuration = {"groups": [], "cards": []}
    for group in groups:
        configuration["groups"].append({"name": group.name})
    for card in cards:
        the_card = dict()
        the_card["name"] = card.name
        the_card["group"] = card.group.name
        if len(card.description):
            the_card["description"] = card.description
        if len(card.url):
            the_card["url"] = card.url
        if card.image:
            the_card["image"] = card.image
        # Status
        if card.status_enable:
            the_card["status_enable"] = card.status_enable
            if len(card.status_url):
                the_card["status_url"] = card.status_url
            if card.status_code:
                the_card["status_code"] = card.status_code
            if card.status_freq:
                the_card["status_freq"] = card.status_freq
        # Docker
        if len(card.docker_server_url):
            the_card["docker_server_url"] = card.docker_server_url
            if card.docker_env:
                the_card["docker_env"] = card.docker_env
            if card.docker_container_name:
                the_card["docker_container_name"] = card.docker_container_name
        # Done, then append
        configuration["cards"].append(the_card)

    # Now write the conf yml file
    fullname = settings.HF_DASHBOARD_CARDS_FILE
    with open(fullname, "w") as yaml_file:
        yaml.dump(configuration, yaml_file)
