from django.contrib import admin
from django.contrib.auth.models import User

from usermanagement.forms import UserCreateForm

#admin.site.unregister(User)

class UserAdmin(admin.ModelAdmin):
  add_form = UserCreateForm
  #fieldsets = (
  #    (None, {
  #      #'classes': ('wide',),
  #      #'fields': ('username', 'email', 'password',)
  #      }),
  #    )
  #list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
  search_fields = ('username', 'first_name', 'last_name', 'email')

#admin.site.register(User, UserAdmin)
