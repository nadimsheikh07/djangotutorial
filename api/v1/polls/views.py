from django.db.models import F
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from polls.models import Question, Choice
from .serializers import QuestionSerializer


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )


class QuestionDetailView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class VoteView(APIView):
    def post(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND
            )

        choice_id = request.data.get("choice")

        if not choice_id:
            return Response(
                {"error": "Choice is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            selected_choice = question.choice_set.get(pk=choice_id)
        except Choice.DoesNotExist:
            return Response(
                {"error": "Invalid choice"}, status=status.HTTP_400_BAD_REQUEST
            )

        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        return Response({"message": "Vote counted successfully"})
