from django.urls import path

from . import views

urlpatterns = [
    path("", views.challenges, name="challenges"),
    path("start_challenge/", views.start_challenge, name="start_challenge"),
    path("<int:id>/", views.challenge, name="challenge"),
    path("remove_challenge/<int:id>", views.remove_challenge, name="remove_challenge"),
    path("report/<int:challenge_id>/", views.report, name="report"),
]
