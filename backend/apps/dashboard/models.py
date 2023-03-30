from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Vote(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()
    
    def __str__(self):
        return self.question

class Answer(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return self.text

class VoteChoice(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    votes = models.ManyToManyField(Vote, blank=True)