from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="dashboard"),
    path('edit_mode_menu/', views.edit_mode_menu, name='edit_mode_menu'),

    path('card_create/<group_name>', views.card_create, name='card_create'),
    path('card_delete/<card_id>', views.card_delete, name='card_delete'),
    path('card_status/<card_id>', views.card_status, name='card_status'),
    path('card_list', views.card_list, name='card_list'),
    path('card_edit_popup/<card_id>', views.card_edit_popup, name='card_edit_popup'),


    path('group_create', views.group_create, name='group_create'),
    path('group_delete/<group_id>', views.group_delete, name='group_delete'),

    # path('addchannel/<channel_id>/', views.add_channel, name='add-channel'),
    # path('generate/', views.generate, name='generate'),
    # path('get_progress/<task_id>/', views.get_progress, name='get-progress'),
    # path('delete_channel/<channel_id>/', views.deletechannel, name='delete-channel'),

    # path('schedule', views.schedule_task, name='schedule'),
]
