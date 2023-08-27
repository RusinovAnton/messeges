from django.http import HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ChatRoom, Message, Thread


def index(request, room_name=None):
    messages = (
        Message.objects.select_related("user")
        .filter(parent_thread__isnull=True)
        .order_by("sent_at")
    )

    reply_to_id = request.GET.get("reply_to")
    reply_to = messages.filter(id=reply_to_id).first() if reply_to_id else None

    room = None
    if room_name:
        room = get_object_or_404(ChatRoom, name=room_name)

    messages_list = []
    for message in messages:
        message.thread = message.thread_set.first()
        messages_list.append(message)

    context = {
        "room_name": room_name,
        "room": room,
        "messages": messages_list,
        "reply_to": reply_to,
    }

    return render(request, "index.html", context)


def send_message(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    message_text = request.POST["message"]
    message = Message(message=message_text, user=request.user)
    message.save()

    room_name = 'default'

    channel_layer = get_channel_layer()
    group_name = f"chat_{room_name}"

    template = loader.get_template("components/ws-messages-list-item.html")
    context = {
        "message": message,
    }
    htmx = template.render(context, request)


    # Send the message via websocket
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat_message",
            "message": message_text,
            "htmx": htmx,
        }
    )

    return redirect("chat")


def reply_to_message(request, message_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    started_from = get_object_or_404(Message, pk=message_id)

    return_url = request.POST["return_url"]
    message_text = request.POST["message"]
    reply = Message(message=message_text, user=request.user)
    reply.save()

    thread = started_from.thread_set.first()
    if not thread:
        thread = Thread(started_from=started_from)
        thread.save()

    thread.messages.add(reply)
    thread.save()

    return redirect(return_url)

def thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    messages = thread.messages.all()
    started_from = thread.started_from
    context = {
        "started_from": started_from,
        "messages": messages,
        "thread": thread,
    }
    return render(request, "thread.html", context)
