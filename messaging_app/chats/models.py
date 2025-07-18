from django.db import models

# Create your models here.

class conversation (models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class message(models.Model):
    conversation = models.ForeignKey(conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}..."  # Display first 20 characters of content