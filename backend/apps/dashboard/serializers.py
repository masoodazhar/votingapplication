from rest_framework import serializers
from .models import Vote, VoteChoice, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteChoice
        fields = ('id', 'text', 'votes')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'question', 'created_by', 'expired_at', 'choices')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'vote')

    def create(self, validated_data):
        answer = Answer.objects.create(
            text=validated_data['text'],
            vote=validated_data['vote']
        )
        return answer


