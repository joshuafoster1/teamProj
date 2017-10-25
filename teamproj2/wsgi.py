"""
WSGI config for teamproj2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

### Production
# path = '/home/joshuafoster1/teamProj'
# if path not in sys.path:
#     sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamproj2.settings")

application = get_wsgi_application()
