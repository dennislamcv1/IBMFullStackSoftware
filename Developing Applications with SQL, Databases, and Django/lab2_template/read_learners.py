# Django specific settings
import inspect
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.db import connection
# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from crud.models import *
from datetime import date


# Your code starts from here:
 # Find students with last name "Smith"
learners_smith = Learner.objects.filter(last_name="Smith")
print("1. Find learners with last name `Smith`:")
print(learners_smith)
print("\n")
# Order by dob descending, and select the first two objects
learners = Learner.objects.order_by('-dob')[0:2]
print("2. Find top two youngest learners:")
print(learners)