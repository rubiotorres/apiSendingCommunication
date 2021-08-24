from django.db import models


# A models is the skeleton of information about your data.
# Each class that extends `models.Model` represents a table of its fields and behaviors.


class Scheduling(models.Model):
    # Scheduling Data Model
    # id int: pk table
    # date_entry datetime: Message entry date
    # sender string: Name of the user who will send the message
    # date_send string: Message sent date
    # receiver string: Name of the user who will receive the message
    # message string: Message to be sent
    # status string: Message sending status
    class Meta:
        # Table name for this template
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
