import json
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from . import views

from .models import Scheduling

create_julieta = {
    "sender": "Julieta",
    "date_send": "2021-08-19T22:01:05Z",
    "receiver": "Romeu",
    "message": "Oh Romeu"
}

create_romeu = {
    "sender": "Romeu",
    "date_send": "2021-08-19T22:01:05Z",
    "receiver": "Julieta",
    "message": "Oh Julieta"
}
# Create your tests here.


class ScheduleModelTestCase(TestCase):
    def setUp(self):
        Scheduling.objects.create(sender=create_julieta["sender"],
                                  date_send=create_julieta["date_send"],
                                  receiver=create_julieta["receiver"],
                                  message=create_julieta["message"])

    def test_schedule_module(self):
        print("Testing model...")
        romeu = Scheduling.objects.get(sender=create_julieta["sender"])
        # Tests if modules were created correctly.
        self.assertEqual(str(romeu),
                         "This message is going from Julieta to Romeu.\n Day: 2021-08-19 22:01:05+00:00")
        # Tests whether read-only fields have been created.
        self.assertTrue(romeu.date_entry)
        self.assertTrue(romeu.status)


class ScheduleApiTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        self.token = 'Token {}'.format(
            str(Token.objects.get_or_create(user=self.user)[0]))
        Scheduling.objects.all().delete()
        Scheduling.objects.create(sender=create_julieta["sender"],
                                  date_send=create_julieta["date_send"],
                                  receiver=create_julieta["receiver"],
                                  message=create_julieta["message"])

    def test_post(self):
        print("Testing POST: /scheduling/create/ endpoint...")
        view = views.SchedulingCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post('/notes/', create_romeu, format='json')

        response = view(request)
        response.render()

        romeu = Scheduling.objects.get(sender=create_romeu["sender"])

        self.assertEqual(str(request.content_type), "application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(romeu.message), create_romeu["message"])

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
            str(data['data'][0]['date_send']), create_julieta["date_send"])
        self.assertEqual(str(data['data'][0]['message']),
                         create_julieta["message"])
        self.assertEqual(str(data['data'][0]['receiver']),
                         create_julieta["receiver"])
        self.assertEqual(str(data['data'][0]['sender']),
                         create_julieta["sender"])

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
