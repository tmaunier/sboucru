"""
Oxford University Clinical Research Unit
Serum bank manager
MIT License
Copyright (c) 2018 tmaunier
link : https://github.com/tmaunier/sboucru
Written by Tristan Maunier
Bioinformatics Master Degree - University of Bordeaux, France
"""

"""
WSGI config for sboucru project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sboucru.settings")

application = get_wsgi_application()
