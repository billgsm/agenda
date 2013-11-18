from django.contrib import admin

from models import *

class CircleAdmin(admin.ModelAdmin):
  list_display = ('name', 'owner',)

class UserInfoAdmin(admin.ModelAdmin):
  pass
  list_display = ('circles', 'notes',)

class ContactAdmin(admin.ModelAdmin):
  list_display = ('owner', 'user',)

class InvitationAdmin(admin.ModelAdmin):
  list_display = ('email', 'sender',)

admin.site.register(Circle, CircleAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Invitation, InvitationAdmin)

