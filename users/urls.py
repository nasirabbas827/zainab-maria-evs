from django.urls import path
from .views import home, profile, RegisterView
from . import views


urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('view_candidates/<int:election_id>/', views.view_candidates, name='view_candidates'),
    path('vote/<int:candidate_id>/', views.vote, name='vote'),
    path('election_winner/', views.election_winner, name='election_winner'),

]
