from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path("CreateVote", views.create_vote, name="create_vote"),
    path("ViewVote/<int:pk>", views.view_vote, name="view_vote"),
    path("UpdateVote/<int:pk>", views.update_vote, name="update_vote"),
    path("DeleteVote/<int:pk>", views.delete_vote, name="delete_vote"),    
    path('votes/', views.VoteAPIView.as_view(), name='vote-list'),
    # path('votes/<int:vote_id>/questions/', views.QuestionAPIView.as_view(), name='question-list'),
    path('questions/<int:question_id>/choices/', views.ChoiceAPIView.as_view(), name='choice-list'),
    path('choices/<int:choice_id>/answer/', views.AnswerAPIView.as_view(), name='answer-create'),
]
