from django.urls import path
from animal_finder import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('login/', views.login_view, name='login'),
    path('google_login/', views.login_with_google_view, name='google_login'),
]