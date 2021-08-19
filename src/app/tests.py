from django.test import TestCase

from .models import Scheduling


# Create your tests here.
class ScheduleModelTestCase(TestCase):
    def setUp(self):
        Scheduling.objects.create(sender="Julieta", date_send="2021-08-19T22:01:05.107184Z", receiver="Julieta",
                                  message="Oh Romeu")

    def test_schedule_module(self):
        romeu = Scheduling.objects.get(sender="Romeu")
        # Tests if modules were created correctly.
        self.assertEqual(str(romeu),
                         "This message is going from Julieta to Romeu.\n Day: 2021-08-19 22:01:05.107184+00:00")
        # Tests whether read-only fields have been created.
        self.assertTrue(romeu.date_entry)
        self.assertTrue(romeu.status)
