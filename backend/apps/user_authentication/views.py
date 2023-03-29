from django.shortcuts import render, redirect
from . forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login
# Create your views here.

def index(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("dashboard:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:   
        form = UserRegistrationForm()

    return render (request, "registration/register.html", context={"form":form})
