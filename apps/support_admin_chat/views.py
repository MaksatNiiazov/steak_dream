from django.shortcuts import render
from .models import ChatRoom, ChatMessage
# Create your views here.
from django.db.models import Q

# views.py
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize

from ..orders.models import Order


@staff_member_required
def admin_chat_list(request):
    chats = ChatRoom.objects.all()

    # Получаем информацию для каждого чата
    chat_data = []
    for chat in chats:
        last_message = chat.messages.order_by('-timestamp').first()  # Последнее сообщение в чате
        unread_messages_count = chat.messages.filter(is_read=False).count()  # Количество непрочитанных сообщений

        chat_data.append({
            'chat': chat,
            'last_message': last_message,
            'unread_messages_count': unread_messages_count
        })

    context = {
        'chat_data': chat_data
    }

    return render(request, 'admin_chat_list.html', context)

@staff_member_required
def admin_chat(request, pk):
    chat_room = ChatRoom.objects.get(id=pk)
    chat_room.messages.filter(is_read=False).update(is_read=True)

    context = {
        'chat_room': chat_room,
        'chat_messages': chat_room.messages.all().order_by('timestamp'),
        'users': request.user
    }

    return render(request, 'admin_chat.html', context)


def user_chat(request):
    if request.user.is_anonymous:
        print('User is anonymous')
        return render(request, 'user_chat.html')
    chat_room, created = ChatRoom.objects.get_or_create(user=request.user)

    context = {
        'chat_room': chat_room,  # Передаем комнату в шаблон
        'chat_messages': chat_room.messages.all().order_by('timestamp'),  # Передаем список сообщений в шаблон
    }

    return render(request, 'user_chat.html', context)



def get_user_orders(request):
    user_id = request.GET.get('user_id')
    if user_id:
        orders = Order.objects.filter(user_id=user_id)
        data = serialize('json', orders)
        print(data)
        return JsonResponse({'orders': data}, safe=False)
    return JsonResponse({'error': 'No user ID provided'}, status=400)