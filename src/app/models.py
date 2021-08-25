from django.db import models
from .validations import phone_regex_validation, return_type_choices


# A models is the skeleton of information about your data.
# Each class that extends `models.Model` represents a table of its fields and behaviors.

# Scheduling Data Model
# id int: pk table
# date_entry datetime: Message entry date
# sender string: Name of the user who will send the message
# date_send string: Message sent date
# receiver string: Name of the user who will receive the message
# message string: Message to be sent
# status string: Message sending status

class Scheduling(models.Model):
    class Meta:
        # Table name for this template
        db_table = 'Scheduling'

    # Structure data
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, default="push", choices=return_type_choices())
    status = models.CharField(max_length=10, default="Scheduled")

    # Data of the person who sends
    name_sender = models.CharField(max_length=50)

    # Message data    
    date_entry = models.DateTimeField(auto_now_add=True, help_text="yyyy-mm-ddThh:mm:ssZ")
    date_send = models.DateTimeField(help_text="yyyy-mm-ddThh:mm:ssZ")
    message = models.CharField(max_length=200)

    # Data of the person who receives
    name_to_send = models.CharField(max_length=50)
    email_to_send = models.EmailField(blank=True)
    phone_to_send = models.CharField(validators=[phone_regex_validation()], max_length=9,
                                     null=True, blank=True)

    def __str__(self):
        return "This message is going from {} to {}.\n Day: {}".format(self.name_sender, self.name_to_send, self.date_send)
