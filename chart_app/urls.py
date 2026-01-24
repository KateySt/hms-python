from django.urls import path

from chart_app.views import chat_view

urlpatterns = [
    path('room/<str:room_name>/', chat_view, name='chat_view'),
]
