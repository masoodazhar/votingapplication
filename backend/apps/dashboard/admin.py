from django.contrib import admin
from .models import VoteChoice, Vote, Answer, Profile
# Register your models here.

admin.site.register([VoteChoice, Vote, Answer, Profile])