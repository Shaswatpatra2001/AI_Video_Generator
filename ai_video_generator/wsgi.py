"""
WSGI config for ai_video_generator project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_video_generator.settings')

application = get_wsgi_application()