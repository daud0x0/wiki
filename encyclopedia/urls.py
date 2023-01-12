from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("wiki/random", views.random, name="random"),
	path("wiki/<str:title>", views.get_page,name="get_page"),
	path("search", views.search, name="search"),
	path("create", views.create, name="create"),
	path("wiki/<str:entry>/edit", views.edit, name="edit")
]
