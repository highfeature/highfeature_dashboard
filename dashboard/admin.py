from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from dashboard.models import Notification


class SendNotificationForm(forms.Form):
    message = forms.CharField(label="Notification Message", max_length=100)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    add_form_template = "admin/custom_add_form.html"

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            form = SendNotificationForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data["message"]
                # add it into the db
                notification = Notification.objects.create(message=message)
                # send it in the channel
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "notifications", {"type": "send_notification", "message": message}
                )
                return HttpResponseRedirect(f"../{notification.pk}/")
        else:
            form = SendNotificationForm()

        context = self.get_changeform_initial_data(request)
        context["form"] = form
        return super().add_view(request, form_url, extra_context=context)

    def get_urls(self):
        # add the url into the Django url path
        urls = super().get_urls()
        custom_url = [path("send_notification/", self.admin_site.admin_view(self.add_view), name="send-notification")]
        return custom_url + urls
