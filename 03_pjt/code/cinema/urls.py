from django.urls import path
from . import views

app_name = 'cinema'
urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('home/', views.home, name = 'home'),
    path('community/', views.community, name = 'community'),
]
