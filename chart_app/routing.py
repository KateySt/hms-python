from django.urls import re_path

from chart_app.consumers import ChartConsumer

websocket_urlpatterns = [
    re_path(r"ws/chart/(?P<room_name>\w+)/$", ChartConsumer.as_asgi()),
]
