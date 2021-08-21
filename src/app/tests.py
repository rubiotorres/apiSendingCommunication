import json
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from . import views

from .models import Scheduling


# Create your tests here.
class ScheduleModelTestCase(TestCase):
    def setUp(self):
        Scheduling.objects.create(sender="Julieta", date_send="2021-08-19T22:01:05.107184Z", receiver="Romeu",
                                  message="Oh Romeu")

    def test_schedule_module(self):
        romeu = Scheduling.objects.get(sender="Julieta")
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
        self.token = Token.objects.get_or_create(user=self.user)
        Scheduling.objects.all().delete()
        Scheduling.objects.create(sender="Julieta", date_send="2021-08-19T22:01:05.107184Z", receiver="Romeu",
                                  message="Oh Romeu")

    def test_post(self):
        view = views.SchedulingCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post('/notes/', {
            "sender": "Romeu",
            "date_send": "2021-08-19T22:01:05.107184Z",
            "receiver": "Julieta",
            "message": "Oh Julieta"
        }, format='json')

        response = view(request)
        response.render()

        julieta = Scheduling.objects.get(sender="Julieta")

        self.assertEqual(str(request.content_type),"application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(julieta.message), "Oh Romeu")

    def test_get_list(self):
        view = views.SchedulingSearchList.as_view()

        factory = APIRequestFactory()
        request = factory.get('/scheduling/search/', HTTP_AUTHORIZATION='Token {}'.format(str(self.token[0])))
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
        self.assertEqual(str(data['data'][0]['date_send']), "2021-08-19T22:01:05Z")
        self.assertEqual(str(data['data'][0]['message']), "Oh Romeu")
        self.assertEqual(str(data['data'][0]['receiver']), "Romeu")
        self.assertEqual(str(data['data'][0]['sender']), "Julieta")

    def test_get_id(self):
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
        view = views.SchedulingDelete.as_view()

        factory = APIRequestFactory()
        request = factory.delete('/scheduling/delete/', HTTP_AUTHORIZATION='Token {}'.format(str(self.token[0])))
        force_authenticate(request, user=self.user)
        response = view(request, pk='1')
        response.render()

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check for responses.
        self.assertFalse(Scheduling.objects.all().exists())
