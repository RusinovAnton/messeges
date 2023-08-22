from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="chat"),
    path("send/", views.send_message, name="send_message"),
    path("<int:message_id>/reply", views.reply_to_message, name="reply_to_message"),
    path("thread/<int:thread_id>", views.thread, name="thread"),
]
