from django.urls import path
from . import views

app_name = 'userAuth'
urlpatterns = [
    path("", views.index, name="register"),
     path('login/', views.LoginAPIView.as_view(), name='loginApi'),
     path('register/', views.RegisterAPIView.as_view(), name='registerApi'),
]
