from django.urls import path, include

urlpatterns = [
    path("polls/", include("api.v1.polls.urls")),
]
