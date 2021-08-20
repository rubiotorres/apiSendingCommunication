from django.db import models


# Create your models here.


class Scheduling(models.Model):
    class Meta:
        db_table = 'Scheduling'

    id = models.AutoField(primary_key=True)
    date_entry = models.DateTimeField(auto_now_add=True, help_text="yyyy-mm-ddThh:mm:ssZ")
    sender = models.CharField(max_length=50)
    date_send = models.DateTimeField()
    receiver = models.CharField(max_length=50)
    message = models.CharField(max_length=200)
    status = models.CharField(max_length=10, default="Scheduled")

    def __str__(self):
        return "This message is going from {} to {}.\n Day: {}".format(self.sender, self.receiver, self.date_send)
