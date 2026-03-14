from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all),
    path("tratar_word", views.tratar_palavra),
    
]
