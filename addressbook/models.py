from django.db import models
from django.contrib.auth.models import User

class Circle(models.Model):
  name = models.CharField(max_length=250)
  owner = models.ForeignKey(User)

  def contacts(self):
    """
    - return users who belong to the circle
    """
    return self.user_info.contact_set.all()

  def is_in_circle(self, user):
    if user in self.user_info.contact_set.all():
      return True
    return False


class UserInfo(models.Model):
  circle = models.ManyToManyField(Circle)
  notes = models.TextField()


class Contact(models.Model):
  """
  Entrypoint of the addressbook
  """
  # User to whom belongs the contact
  owner = models.ForeignKey(User)
  # Django user whom this contact refer to
  user = models.ForeignKey(User, related_name='friend')
  invitation_sent = models.BooleanField()
  invitation_accepted = models.BooleanField()
  optional_informations = models.OneToOneField(UserInfo, blank=True, null=True)

  def all_contacts(self, user):
    """
    - All contacts of the user
    """
    return Contact.objects.filter(owner=user)

  def all_circles(self, user):
    """
    - All circles of the user
    """
    return Circle.objects.filter(owner=user)

class Invitation(models.Model):
  email = models.EmailField()
  sender = models.ForeignKey(User)

  def __unicode__(self):
    return self.email

  def get_absolute_url(self):
    return reverse('invitation_list')

  class Meta:
    unique_together = ('email', 'sender')
