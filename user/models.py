from django.db import models
from adminuser.models import Usermember

class Visitor(models.Model):
    Visited = models.ForeignKey(Usermember, on_delete=models.CASCADE, related_name='visited_set')
    Visitor = models.ForeignKey(Usermember, on_delete=models.CASCADE, related_name='visitor_set')
    Time = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    Sender = models.ForeignKey(Usermember, related_name='sent_messages', on_delete=models.CASCADE)
    Receiver = models.ForeignKey(Usermember, related_name='received_messages', on_delete=models.CASCADE)
    Content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
class Message_Request(models.Model):
    Sender = models.ForeignKey(Usermember, related_name='sent_request', on_delete=models.CASCADE)
    Receiver = models.ForeignKey(Usermember, related_name='received_request', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_request = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_notify=models.BooleanField(default=False)
    