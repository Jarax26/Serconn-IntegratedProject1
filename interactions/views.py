from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Chat, Message, Booking, Notification
from accounts.models import User
from searching.models import Service
from django.db.models import Q, Count

@login_required
def create_or_find_chat(request, provider_id):
    provider = get_object_or_404(User, id=provider_id)
    
    chat = Chat.objects.filter(seeker=request.user, provider=provider).first()
        
    if not chat:
        chat = Chat.objects.create(seeker=request.user, provider=provider)
        
    return redirect('chat_view', chat_id=chat.id)

@login_required
def empty_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Medida de seguridad: solo los participantes del chat pueden vaciarlo
    if request.user != chat.seeker and request.user != chat.provider:
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

    if request.method == 'POST':
        chat.messages.all().delete()
        messages.info(request, 'El chat ha sido vaciado.')
    
    return redirect('chat_view', chat_id=chat.id)

@login_required
def chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by('timestamp')
    return render(request, 'chat.html', {'chat': chat, 'messages': messages})

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat=chat, sender=request.user, content=content)
    return redirect('chat_view', chat_id=chat.id)

@login_required
def create_booking(request, chat_id, service_id):
    chat = get_object_or_404(Chat, id=chat_id)
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        notes = request.POST.get('notes')
        
        booking = Booking.objects.create( 
            chat=chat,
            service=service,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )

        Notification.objects.create(
            recipient=chat.provider,
            booking=booking,
            message=f"Tienes una nueva solicitud de servicio de {request.user.get_full_name()} para '{service.name}'."
        )
        messages.success(request, 'Tu solicitud ha sido enviada con éxito.')
        return redirect('dashboard')

    return render(request, 'booking_form.html', {'chat': chat, 'service': service})

@login_required
def respond_to_booking(request, booking_id, response):
    booking = get_object_or_404(Booking, id=booking_id, chat__provider=request.user)
    
    if response == 'accept':
        booking.status = 'confirmed'
        message_to_seeker = f"Tu solicitud para '{booking.service.name}' ha sido aceptada por el proveedor."
        messages.success(request, 'Has aceptado la solicitud.')
    else:
        booking.status = 'rejected'
        message_to_seeker = f"Tu solicitud para '{booking.service.name}' ha sido rechazada."
        messages.error(request, 'Has rechazado la solicitud.')
    
    booking.save()

    Notification.objects.create(
        recipient=booking.chat.seeker,
        booking=booking,
        message=message_to_seeker
    )
    
    return redirect('dashboard')

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    notifications.update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def cancel_booking(request, booking_id):
    # Asegurarse de que solo el solicitante pueda cancelar
    booking = get_object_or_404(Booking, id=booking_id, chat__seeker=request.user)
    
    if request.method == 'POST':
        # Cambia el estado en lugar de eliminar
        booking.status = 'cancelled'
        booking.save()

        # Crear la notificación para el proveedor
        Notification.objects.create(
            recipient=booking.chat.provider,
            booking=booking,
            message=f"El cliente {booking.chat.seeker.get_full_name()} ha cancelado la solicitud para el servicio '{booking.service.name}'."
        )

        messages.success(request, 'La solicitud de servicio ha sido cancelada correctamente.')
        return redirect('dashboard')

    # Redirigir si no es POST para evitar cancelaciones accidentales por GET
    return redirect('dashboard')

@login_required
def chat_list(request):
    """
    Muestra la lista de conversaciones activas (con mensajes) para un usuario.
    """
    # Obtiene los chats del usuario y los filtra para mostrar solo los que no están vacíos
    chats = Chat.objects.filter(
        Q(provider=request.user) | Q(seeker=request.user)
    ).annotate(
        message_count=Count('messages')
    ).filter(
        message_count__gt=0
    ).order_by('-created_at')
    
    return render(request, 'chat_list.html', {'chats': chats})