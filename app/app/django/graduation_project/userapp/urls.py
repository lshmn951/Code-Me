from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_search_index, name='user_search_index'),
    path('user', views.user_search, name='user_search'),
]
