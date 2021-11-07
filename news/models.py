from django.db import models


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    post = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime',)

    def __str__(self):
        return self.title