import json
from django.test import TestCase

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
                         "This message is going from Julieta to Romeu.\n Day: 2021-08-19 22:01:05.107184+00:00")
        # Tests whether read-only fields have been created.
        self.assertTrue(romeu.date_entry)
        self.assertTrue(romeu.status)


class ScheduleApiTestCase(TestCase):
    def setUp(self):
        Scheduling.objects.all().delete()
        Scheduling.objects.create(sender="Julieta", date_send="2021-08-19T22:01:05.107184Z", receiver="Romeu",
                                  message="Oh Romeu")

    def test_post(self):
        response = self.client.post(
            '/scheduling/create/',
            {
                "sender": "Romeu",
                "date_send": "2021-08-19T22:01:05.107184Z",
                "receiver": "Julieta",
                "message": "Oh Julieta"
            },
        )
        julieta = Scheduling.objects.get(sender="Julieta")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(julieta.message), "Oh Romeu")

    def test_get_list(self):
        response = self.client.get(
            '/scheduling/search/'
        )
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check Number of responses.
        self.assertEqual(len(data['data']), 1)
        # Check data integrity(date_send).
        self.assertEqual(str(data['data'][0]['date_send']), "2021-08-19T22:01:05.107184Z")
        self.assertEqual(str(data['data'][0]['message']), "Oh Romeu")
        self.assertEqual(str(data['data'][0]['receiver']), "Romeu")
        self.assertEqual(str(data['data'][0]['sender']), "Julieta")

    def test_get_id(self):
        response = self.client.get(
            '/scheduling/search/id/2'
        )
        response_json = response.content.decode('utf8').replace("'", '"')
        data = json.loads(response_json)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check Number of responses.
        self.assertEqual(len(data['data']), 7)

    def test_delete_id(self):
        response = self.client.delete(
            '/scheduling/delete/1'
        )
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 204)
        # Check for responses.
        self.assertFalse(Scheduling.objects.all().exists())
