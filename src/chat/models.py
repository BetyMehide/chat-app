from datetime import date

from django.db import models
from django.urls import reverse
from django.utils import timezone


class ConversationModel(models.Model):
    title = models.CharField(max_length=280, unique=True, blank=False)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(default=date.today)

    def get_absolute_url(self):
        return reverse("chat:messages", kwargs={"id": self.id})


class MessageModel(models.Model):
    conversation_id = models.ForeignKey(ConversationModel, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    date_time = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("chat:thoughts", kwargs={"id": self.id})


class ThoughtModel(models.Model):
    message_id = models.ForeignKey(MessageModel, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    date_time = models.DateTimeField(default=timezone.now)
