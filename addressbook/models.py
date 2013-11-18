from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

class Circle(models.Model):
  name = models.CharField(max_length=250)
  owner = models.ForeignKey(User)

  def contacts(self):
    """
    - return users who belong to the circle
    """
    return self.userinfo_set.all()

  def is_in_circle(self, user):
    """
    * True if the user belongs to the circle
    """
    if user in self.userinfo_set.all():
      return True
    return False

  def __unicode__(self):
    return u'{0}'.format(self.name)

  def get_absolute_url(self):
    return reverse('circle_detail', kwargs={'pk': self.pk})


class UserInfo(models.Model):
  circle = models.ManyToManyField(Circle, null=True, blank=True)
  notes = models.TextField()

  def __unicode__(self):
    return u'{0}'.format(self.notes)

  def circles(self):
    return ', '.join((circle.name for circle in self.circle.all()))


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

  def get_absolute_url(self):
    return reverse('contact_detail', kwargs={'pk': self.pk})

  def __unicode__(self):
    return u'owner: {0}, user: {1}'.format(self.owner, self.user)

  def save(self, *args, **kwargs):
    super(Contact, self).save(*args, **kwargs)
    if self.optional_informations == None:
      infos = UserInfo.objects.create()
      self.optional_informations = infos
      self.save()
      infos.save()

  def delete(self, *args, **kwargs):
    optional_informations = self.optional_informations
    super(Contact, self).delete(*args, **kwargs)
    optional_informations.delete()


class Invitation(models.Model):
  email = models.EmailField()
  sender = models.ForeignKey(User)

  def __unicode__(self):
    return u'{0}'.format(self.email)

  def get_absolute_url(self):
    return reverse('invitation_detail', kwargs={'pk': self.pk})

  def all_invitations(self, user):
    return Invitation.objects.filter(sender=user)

  class Meta:
    unique_together = ('email', 'sender')

def create_contact_on_user_create(sender, instance, created, **kwargs):
  if created == True:
    try:
      invitations = Invitation.objects.filter(email=instance.email)
      for invitation in invitations:
        contact = Contact(owner=invitation.sender, user=instance)
        contact.save()
        invitation.delete()
    except Invitation.DoesNotExist:
      pass

post_save.connect(create_contact_on_user_create, sender=User)

