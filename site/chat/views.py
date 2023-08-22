from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, Thread


def index(request):
    user = request.user
    if user.is_anonymous:
        return redirect("signin")

    messages = (
        Message.objects.select_related("user")
        .filter(parent_thread__isnull=True)
        .order_by("sent_at")
    )

    reply_to_id = request.GET.get("reply_to")
    reply_to = messages.filter(id=reply_to_id).first() if reply_to_id else None

    messages_list = []
    for message in messages:
        message.thread = message.thread_set.first()
        messages_list.append(message)

    context = {
        "messages": messages_list,
        "reply_to": reply_to,
    }
    return render(request, "index.html", context)


def send_message(request):
    message_text = request.POST["message"]
    message = Message(message=message_text, user=request.user)
    message.save()
    print(message)

    return redirect("chat")


def reply_to_message(request, message_id):
    started_from = get_object_or_404(Message, pk=message_id)

    message_text = request.POST["message"]
    reply = Message(message=message_text, user=request.user)
    reply.save()

    thread = started_from.thread_set.first()
    if not thread:
        thread = Thread(started_from=started_from)
        thread.save()

    thread.messages.add(reply)
    thread.save()

    return redirect("chat")
