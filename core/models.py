from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
	started_by = models.ForeignKey(User, on_delete = models.CASCADE)
	sent_to = models.ForeignKey(User, on_delete = models.CASCADE, related_name ='received_by')
	timestamp = models.DateTimeField(auto_now_add=True)
	chatroom = models.TextField(blank=True)


	class Meta:
		unique_together = (("started_by", "sent_to"))

	def __str__(self):
		return self.chatroom

	@staticmethod
	def check_conversation(user1, user2):
		user1_obj = User.objects.get(username = user1)
		user2_obj = User.objects.get(username = user2)
		if Conversation.objects.filter(started_by = user1_obj, sent_to = user2_obj).count():
			data = Conversation.objects.get(started_by = user1_obj, sent_to = user2_obj)
		elif Conversation.objects.filter(started_by = user2_obj, sent_to = user1_obj).count():
			data = Conversation.objects.get(started_by = user2_obj, sent_to = user1_obj)
		else:
			data = None

		return data



class Message(models.Model):
	conv_id = models.ForeignKey(Conversation, on_delete = models.CASCADE)
	text = models.TextField(blank=True)
	sender = models.ForeignKey(User, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text
