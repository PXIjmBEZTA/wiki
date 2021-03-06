from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:Title>", views.entry, name="entry"),
    path("create", views.create, name="create")
]
