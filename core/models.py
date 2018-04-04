from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
	started_by = models.ForeignKey(User, on_delete = models.CASCADE)
	sent_to = models.ForeignKey(User, on_delete = models.CASCADE, related_name ='received_by')
	timestamp = models.DateTimeField(auto_now_add=True)


	class Meta:
		unique_together = (("started_by", "sent_to"))

class Message(models.Model):
	conv_id = models.ForeignKey(Conversation, on_delete = models.CASCADE)
	text = models.TextField(blank=True)
	sender = models.ForeignKey(User, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)
