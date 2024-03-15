from django.contrib import admin
from .models import UserProfile, Document, Staff

admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(Staff)
