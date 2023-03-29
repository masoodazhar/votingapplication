from django.urls import path
from . import views

app_name = 'userAuth'
urlpatterns = [
    path("", views.index, name="register")
]
