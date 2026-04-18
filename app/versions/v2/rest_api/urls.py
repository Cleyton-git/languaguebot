from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all),
    path("bot_end/", views.chatbot_telegram),
]
