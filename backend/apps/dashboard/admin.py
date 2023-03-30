from django.contrib import admin
from .models import VoteChoice, Vote
# Register your models here.

admin.site.register([VoteChoice, Vote])