from django.contrib import admin

from models import Evenement, Evenement_Participant

class EvenementAdmin(admin.ModelAdmin):
  pass

class Evenement_ParticipantAdmin(admin.ModelAdmin):
  pass

admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Evenement_Participant, Evenement_ParticipantAdmin)
