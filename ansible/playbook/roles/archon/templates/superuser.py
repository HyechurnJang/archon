import os
import sys

# First, add the project to PATH. Adjust as needed.
PWD = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(PWD, 'archon'))
sys.path.append(PROJECT_PATH)

# Second, configure this script to use Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archon.settings')

try:
    django.setup()
except AttributeError:
    print django.VERSION

from django.contrib.auth.management.commands import changepassword
from django.core import management
from django.contrib.auth.models import User

User.objects.create_superuser('admin', 'hyungsok@cisco.com', '{{database_pass}}')
