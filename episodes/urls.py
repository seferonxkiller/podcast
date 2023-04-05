from django.urls import path
from .views import index, episodes_detail, get_ids_list, like

app_name = 'episodes'

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:pk>/', episodes_detail, name='detail'),
    path('ids_list/', get_ids_list, name='get_ids_list'),
    path('like/', like, name='like'),
]