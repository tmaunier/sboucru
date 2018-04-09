from django.contrib import admin

# Register your models here.
from .models import Serum, Site, Ward, Freezer

admin.site.register(Serum)
admin.site.register(Site)
admin.site.register(Ward)
admin.site.register(Freezer)
