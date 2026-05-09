from django.urls import path
from . import views

urlpatterns = [
    path("bot_end/", views.chatbot_telegram),
]
