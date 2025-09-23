from django.urls import path
from . import views

urlpatterns = [
    path('chat/start/<int:provider_id>/', views.create_or_find_chat, name='create_or_find_chat'),
    path('chat/<int:chat_id>/', views.chat_view, name='chat_view'),
    path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:chat_id>/empty/', views.empty_chat, name='empty_chat'),
    path('chats/', views.chat_list, name='chat_list'),
    path('booking/create/<int:chat_id>/<int:service_id>/', views.create_booking, name='create_booking'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking/respond/<int:booking_id>/<str:response>/', views.respond_to_booking, name='respond_to_booking'),
    path('notifications/', views.notification_list, name='notification_list'),
]