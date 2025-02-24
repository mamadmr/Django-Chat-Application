from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

User = get_user_model()

class Conversation(models.Model):
    participants = models.ManyToManyField(User, through='ConversationParticipant')
    created_at = models.DateTimeField(auto_now_add=True)

class ConversationParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    allowed_message_types = models.ManyToManyField(ContentType)
    messages_per_minute = models.PositiveIntegerField(default=10)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

class MessageSeenStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    seen_at = models.DateTimeField(auto_now_add=True)




class BaseMessageContent(models.Model):
    message = GenericRelation(Message, content_type_field='content_type', object_id_field='object_id')
    
    class Meta:
        abstract = True

class TextMessage(BaseMessageContent):
    text = models.TextField()

class FileMessage(BaseMessageContent):
    file = models.FileField(upload_to='messenger_files/')
