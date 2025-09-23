from .models import Notification

def unread_notifications_count(request):
    """
    Hace que el número de notificaciones no leídas esté disponible en todas las plantillas.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_notifications': count}
    return {'unread_notifications': 0}