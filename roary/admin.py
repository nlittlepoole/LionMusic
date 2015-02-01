from django.contrib import admin

# Register your models here.
from roary.models import User,Song

admin.site.register(User)
admin.site.register(Song)
