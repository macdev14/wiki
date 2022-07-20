from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new",views.wikiNewPage, name="wikiNewPage"),
    path("wiki/edit",views.wikiEditPage, name="wikiEditPage"),
    path("wiki/random", views.randomPage, name="randomPage"),
    path("wiki/<str:entry>",views.entryPage, name="entryPage"),
    path("wiki",views.entryPage, name="srchPage"),
   
]
