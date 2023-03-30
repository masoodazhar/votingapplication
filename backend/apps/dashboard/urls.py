from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path("CreateVote", views.create_vote, name="create_vote"),
    path("ViewVote/<int:pk>", views.view_vote, name="view_vote"),
    path("UpdateVote/<int:pk>", views.update_vote, name="update_vote"),
    path("DeleteVote/<int:pk>", views.delete_vote, name="delete_vote"),
]
