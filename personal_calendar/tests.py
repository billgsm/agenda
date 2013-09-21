#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from models import Evenement_Participant, Evenement


class TestEvenement_Participant(TestCase):
  def test_create_user(self):
    """
    We need a user as participant to an event,
    let's try to create it
    """
    participant1 = User(first_name="John", last_name="Doe")
    participant1.save()
    # test what has just been saved
    participant = User.objects.get(first_name="John")
    self.assertEqual(participant.last_name, 'Doe')

  def test_create_event(self):
    event = Evenement(nom="new event", description="""\
        this new event is created to show the way unittests work.
        As we aren't in docstring anymore""", date=datetime.now(), lieu="Any location")
    event.save()

    event = Evenement.objects.get(nom="new event")
    self.assertEqual(event.lieu, u'Any location')

  def test_create_event_participant(self):
    self.test_create_user()
    self.test_create_event()
    participant = User.objects.get(first_name='John')
    event = Evenement.objects.get(nom='new event')
    event_part = Evenement_Participant(evenement=event,
                                       participant=participant,
                                       status=1)
    event_part.save()
    event_part = Evenement_Participant.objects.get(evenement=event,
                                                   participant=participant
                                                  )
    self.assertEqual(event_part.status, 1)
