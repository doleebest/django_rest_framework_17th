from django.contrib import admin

from .models import User

# Now register the new UserAdmin...
admin.site.register(User)
