from dateutil import parser
from django.core.validators import RegexValidator
from django.utils import timezone


# Create your validation and regex here.
def phone_regex_validation():
    return RegexValidator(
        regex=r'^\d{9}$',
        message='Phone number must be entered in the format: 999999999'
    )


def return_type_choices():
    return (
        ("Email", "Email"),
        ("SMS", "SMS"),
        ("Push", "Push"),
        ("Whatsapp", "Whatsapp")
    )


def create_validator(request):
    if request.data['type'] == 'Email' \
            and request.data['email_to_send'] == '':
        return (False, 'Please make sure you have entered the correct email '
                       'address or change the submission type.')
    elif (request.data['type'] == 'SMS' or request.data['type'] == 'Whatsapp') \
            and request.data['phone_to_send'] == '':
        return False, 'Please make sure you have entered the correct phone number or change the shipping type.'
    elif timezone.now().replace(tzinfo=None) > parser.parse(request.data['date_send']).replace(tzinfo=None):
        return False, 'Check that the scheduled date is not in the past.'

    else:
        return True, 'Your message has been scheduled.'
