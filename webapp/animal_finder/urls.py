from django.urls import path
from animal_finder import views

urlpatterns = [
    path('', views.index_view, name='index'),
]