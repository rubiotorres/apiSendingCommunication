from django.db import models


# Create your models here.


class Scheduling(models.Model):

    class Meta:

        db_table = 'Scheduling'

    date_entry = models.DateTimeField(auto_now_add=True)    
    sender = models.CharField(max_length=50)
    date_send = models.DateTimeField()
    receiver = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
    status = models.CharField(max_length=10,default="Scheduled")

    def __str__(self):
        return self.title