import json
from datetime import datetime, timedelta
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from . import views

from .models import Scheduling

create_julieta_push = {
    "type": "Push",
    "name_sender": "Julieta",
    "date_send": (datetime.now() + timedelta(days=1, hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "message": "Oh Romeu",
    "name_to_send": "Romeu",
    "email_to_send": "",
    "phone_to_send": ""
}

create_romeu_push = {
    "type": "Push",
    "name_sender": "Romeu",
    "date_send": (datetime.now() + timedelta(days=1, hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "message": "Oh Julieta",
    "name_to_send": "Julieta",
    "email_to_send": "",
    "phone_to_send": ""
}


# Create your tests here.
class ScheduleModelTestCase(TestCase):
    # Basic model test
    def setUp(self):
        Scheduling.objects.create(name_sender=create_julieta_push["name_sender"],
                                  date_send=create_julieta_push["date_send"],
                                  message=create_julieta_push["message"],
                                  name_to_send=create_julieta_push["name_to_send"],
                                  email_to_send=create_julieta_push["email_to_send"],
                                  phone_to_send=create_julieta_push["phone_to_send"]
                                  )

    def test_schedule_module(self):
        print("Testing model...")
        romeu = Scheduling.objects.get(name_sender=create_julieta_push["name_sender"])
        # Tests whether read-only fields have been created.
        self.assertTrue(romeu.date_entry)
        self.assertTrue(romeu.status)


class SchedulePostTestCase(TestCase):
    # Test every POST end point
    def setUp(self):
        self.view = views.SchedulingCreate.as_view()
        self.factory = APIRequestFactory()
        self.dict_fail = create_romeu_push.copy()

    # Test a right post to schedule a message
    def test_post(self):
        print("Testing POST: /scheduling/create/ endpoint...")

        self.dict_fail['type'] = "Push"
        self.dict_fail['date_send'] = (datetime.now() + timedelta(days=1, hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")

        request = self.factory.post('/scheduling/create/', self.dict_fail, format='json')

        response = self.view(request)
        response.render()
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)

        self.assertEqual(data["data"]["status"], "Scheduled")
        self.assertEqual(str(request.content_type), "application/json")
        self.assertEqual(response.status_code, 200)

    # Test a old date fail
    def test_post_fail_date(self):
        self.dict_fail['type'] = "Push"
        self.dict_fail['date_send'] = "2021-08-19T22:01:05Z"

        request = self.factory.post('/scheduling/create/', self.dict_fail, format='json')

        response = self.view(request)
        response.render()
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)

        self.assertEqual(data['message'], 'Your message cannot be scheduled. Check that the scheduled date is not in '
                                          'the past.')

        self.assertEqual(data['status'], 400)

    # Test create a email sender without email
    def test_post_fail_email(self):
        self.dict_fail['type'] = "Email"

        request = self.factory.post('/scheduling/create/', self.dict_fail, format='json')

        response = self.view(request)
        response.render()
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)
        self.assertEqual(data['message'], 'Your message cannot be scheduled. Please make sure you have entered the '
                                          'correct email address or change the submission type.')
        self.assertEqual(data['status'], 400)

    # Test SMS sender without number
    def test_post_fail_number(self):
        self.dict_fail['type'] = "SMS"

        request = self.factory.post('/scheduling/create/', self.dict_fail, format='json')

        response = self.view(request)
        response.render()
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)

        self.assertEqual(data['message'], 'Your message cannot be scheduled. Please make sure you have entered the '
                                          'correct phone number or change the shipping type.')
        self.assertEqual(data['status'], 400)


class ScheduleGetTestCase(TestCase):
    # Test every GET end point
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        self.token = 'Token {}'.format(
            str(Token.objects.get_or_create(user=self.user)[0]))
        Scheduling.objects.create(name_sender=create_julieta_push["name_sender"],
                                  date_send=create_julieta_push["date_send"],
                                  message=create_julieta_push["message"],
                                  name_to_send=create_julieta_push["name_to_send"],
                                  email_to_send=create_julieta_push["email_to_send"],
                                  phone_to_send=create_julieta_push["phone_to_send"]
                                  )

    # Test get list of schedule
    def test_get_list(self):
        print("Testing GET: /scheduling/search/ endpoint...")

        view = views.SchedulingSearchList.as_view()

        factory = APIRequestFactory()
        request = factory.get(
            '/scheduling/search/', HTTP_AUTHORIZATION=self.token)
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()

        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check Number of responses.
        self.assertEqual(len(data['data']), 1)
        # Check data integrity(date_send).
        self.assertEqual(
            str(data['data'][0]['date_send']), create_julieta_push["date_send"])
        self.assertEqual(str(data['data'][0]['message']),
                         create_julieta_push["message"])
        self.assertEqual(str(data['data'][0]['name_to_send']),
                         create_julieta_push["name_to_send"])
        self.assertEqual(str(data['data'][0]['name_sender']),
                         create_julieta_push["name_sender"])

    # Test get a message scheduled by id
    def test_get_id(self):
        print("Testing GET: /scheduling/status/id/ endpoint...")

        view = views.SchedulingSearchId.as_view()
        factory = APIRequestFactory()
        request = factory.get('/scheduling/status/id/')
        response = view(request, pk='2')
        response.render()
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check Number of responses.
        self.assertEqual(data['status'], 'Scheduled')


class ScheduleDeleteTestCase(TestCase):
    # Test a DELETE end point
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        self.token = 'Token {}'.format(
            str(Token.objects.get_or_create(user=self.user)[0]))
        Scheduling.objects.create(name_sender=create_julieta_push["name_sender"],
                                  date_send=create_julieta_push["date_send"],
                                  message=create_julieta_push["message"],
                                  name_to_send=create_julieta_push["name_to_send"],
                                  email_to_send=create_julieta_push["email_to_send"],
                                  phone_to_send=create_julieta_push["phone_to_send"]
                                  )

    def test_delete_id(self):
        print("Testing DELETE: /sscheduling/delete/id/ endpoint...")

        view = views.SchedulingDelete.as_view()

        factory = APIRequestFactory()
        request = factory.delete(
            '/scheduling/delete/id', HTTP_AUTHORIZATION=self.token)
        force_authenticate(request, user=self.user)
        response = view(request, pk='1')
        response.render()
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check for responses.
        self.assertFalse(Scheduling.objects.all().exists())
