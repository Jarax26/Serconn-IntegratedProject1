from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Chat, Message, Booking
from accounts.models import User
from searching.models import Service

@login_required
def create_or_find_chat(request, provider_id):
    provider = get_object_or_404(User, id=provider_id)
    
    chat = Chat.objects.filter(seeker=request.user, provider=provider).first()
    
    if chat:
        chat.messages.all().delete()
    else:
        chat = Chat.objects.create(seeker=request.user, provider=provider)
        
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
        
        Booking.objects.create(
            chat=chat,
            service=service,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )

        return redirect('dashboard')

    return render(request, 'booking_form.html', {'chat': chat, 'service': service})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, chat__seeker=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'La solicitud de servicio ha sido cancelada correctamente.')
        return redirect('dashboard')

    return redirect('dashboard')

@login_required
def chat_list(request):
    """
    Muestra la lista de conversaciones para un proveedor.
    """
    if not request.user.is_service_provider:
        # Si un seeker intenta acceder, lo redirige a su dashboard
        return redirect('dashboard')

    chats = Chat.objects.filter(provider=request.user).order_by('-created_at')
    return render(request, 'chat_list.html', {'chats': chats})