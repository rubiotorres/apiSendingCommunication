from django.db import models

# Create your models here.


class Scheduling(models.Model):

    class Meta:

        db_table = 'Scheduling'

    receiver = models.CharField(max_length=200)
    date = models.DateTimeField()
    message = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.title