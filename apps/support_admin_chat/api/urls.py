# urls.py
from django.urls import path
from .views import admin_chat_list, admin_chat, user_chat
from ..views import get_user_orders

urlpatterns = [
    path('api/admin/chats/', admin_chat_list, name='admin_chat_list'),
    path('api/admin/chats/<int:pk>/', admin_chat, name='admin_chat'),
    path('api/user/chat/', user_chat, name='user_chat'),
    path('get-user-orders/', get_user_orders, name='get_user_orders'),

]
