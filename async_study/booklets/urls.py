from django.urls import path

from . import views

urlpatterns = [
    path("<int:booklet_id>", views.booklet, name="booklet"),
    path("add_booklet/", views.add_booklet, name="add_booklet"),
]
