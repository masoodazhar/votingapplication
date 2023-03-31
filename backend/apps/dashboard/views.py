from django.shortcuts import render, redirect
from .forms import VoteForm, VoteChoiceFormSet
from .models import Vote, Answer
from django.shortcuts import render, get_object_or_404
from django.core.management.base import BaseCommand

# FOR APIs
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Vote, VoteChoice
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .serializers import VoteSerializer, QuestionSerializer, ChoiceSerializer, AnswerSerializer


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

# API Section
class VoteAPIView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Vote.objects.filter(expired_at__gte=timezone.now()).order_by('-pk')


class ChoiceAPIView(generics.ListAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return VoteChoice.objects.filter(vote=question_id)

class AnswerAPIView(generics.GenericAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, choice_id):
        user = request.user
        try:
            vote_choice = VoteChoice.objects.get(id=choice_id)
        except VoteChoice.DoesNotExist:
            return Response({'detail': 'Invalid choice id'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already voted for the vote that contains the choice
        vote = vote_choice.vote
        if vote in user.profile.votes.all():
            return Response({'detail': 'You already voted for this vote.'})
        
        # Create the answer and add it to the vote
        answer = Answer(text=vote_choice.text, vote=vote)
        answer.save()
        
        # Add the vote to the user's votes
        user.profile.votes.add(vote)
        
        return Response({'detail': 'Answer submitted successfully.'})

