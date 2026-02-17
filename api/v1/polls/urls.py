from django.urls import path
from .views import QuestionListView, QuestionDetailView, VoteView

urlpatterns = [
    path("", QuestionListView.as_view(), name="question-list"),
    path("<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path("<int:pk>/vote/", VoteView.as_view(), name="vote"),
]
