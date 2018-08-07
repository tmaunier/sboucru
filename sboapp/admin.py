"""
Oxford University Clinical Research Unit
Serum bank manager
MIT License
Copyright (c) 2018 tmaunier
link : https://github.com/tmaunier/sboucru
Written by Tristan Maunier
Bioinformatics Master Degree - University of Bordeaux, France
"""

from django.contrib import admin
from .models import Serum, Site, Ward, Freezer, Elisa, Chik_elisa, Dengue_elisa, Rickettsia_elisa, Pma, Pma_result

admin.site.register(Serum)
admin.site.register(Site)
admin.site.register(Ward)
admin.site.register(Freezer)
admin.site.register(Elisa)
admin.site.register(Chik_elisa)
admin.site.register(Dengue_elisa)
admin.site.register(Rickettsia_elisa)
admin.site.register(Pma)
admin.site.register(Pma_result)
