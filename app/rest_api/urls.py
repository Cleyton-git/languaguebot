from django.urls import path
from . import views

urlpatterns = [
    path("", views.health),
    path("reminder/", views.Reminder_users),
    path("bot_end/", views.chatbot_telegram),
]
