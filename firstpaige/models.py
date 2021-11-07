from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-datetime',)

    def __str__(self):
        return self.comment
# Create your models here.
