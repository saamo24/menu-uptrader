from django.urls import path
from .views import MenuView

urlpatterns = [
    path('', MenuView.as_view(), name='menu-list'),
    path('<str:menu_name>/', MenuView.as_view(), name='menu-root'),
    path('<str:menu_name>/<path:item_path>/', MenuView.as_view(), name='menu-nested'),
]
