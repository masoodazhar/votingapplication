from django.shortcuts import render, redirect
from .forms import VoteForm, VoteChoiceFormSet
from .models import Vote
from django.shortcuts import render, get_object_or_404
from django.core.management.base import BaseCommand

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')


def create_vote(request):
    votes = Vote.objects.filter(created_by=request.user)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        formset = VoteChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            vote = form.save(commit=False)
            vote.created_by = request.user
            vote.save()
            formset.instance = vote
            formset.save()
            return redirect('dashboard:create_vote')
    else:
        form = VoteForm()
        formset = VoteChoiceFormSet()
    context = {'form': form, 'formset': formset, 'votes': votes}
    return render(request, 'dashboard/create_vote.html', context)


def view_vote(request, pk):
    vote = get_object_or_404(Vote, pk=pk)
    return render(request, 'dashboard/view_vote.html', {'vote': vote})

def update_vote(request, pk):
    vote = get_object_or_404(Vote, pk=pk)
    if request.method == 'POST':
        form = VoteForm(request.POST, instance=vote)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VoteForm(instance=vote)
    return render(request, 'dashboard/update_vote.html', {'form': form})


def delete_vote(request, pk):
    vote = get_object_or_404(Vote, pk=pk, created_by=request.user)
    if request.method == 'POST':
        vote.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/delete_vote.html', {'vote': vote})
