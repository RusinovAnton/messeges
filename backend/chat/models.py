from django.db import models

class ChatRoom(models.Model):
		name = models.CharField(max_length=200)
		created_at = models.DateTimeField(auto_now_add=True)

		def __str__(self):
				return self.name

class Message(models.Model):
		message = models.CharField(max_length=200)
		user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
		room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True)
		sent_at = models.DateTimeField(auto_now_add=True)

		def __str__(self):
				return self.message

class Thread(models.Model):
		started_from = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
		messages = models.ManyToManyField(Message, related_name='parent_thread')

		def __str__(self):
				return self.messages.first().message
