from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_room, name='create_room'),
    path('join/', views.join_room, name='join_room'),
    path('room/<str:code>/', views.room_detail, name='room_detail'),
    path('room/<str:code>/end/', views.end_room, name='end_room'),
    path('about/', views.about, name='about'),
    path('chat/', views.chat_page, name='chat'),
    path('chat/api/', views.chat_api, name='chat_api'),
]
