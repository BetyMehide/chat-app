from django.db import models


class Conversation(models.Model):
    title = models.CharField(max_length=280, unique=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)


class Thought(models.Model):
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
