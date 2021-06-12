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
instructor_yan = Instructor.objects.get(first_name="Yan")
print("1. Find a single instructor with first name `Yan`")
print(instructor_yan)

print("\n")
# Note that there is no instructor with first name `Andy`
# So the manager will throw an exception
try:
    instructor_andy = Instructor.objects.get(first_name="Andy")
except Instructor.DoesNotExist:
    print("2. Try to find a non-existing instructor with first name `Andy`")
    print("Instructor Andy doesn't exist")

print("\n")
part_time_instructors = Instructor.objects.filter(full_time=False)
print("3. Find all part time instructors: ")
print(part_time_instructors)

print("\n")
full_time_instructors = Instructor.objects.exclude(full_time=False).filter(total_learners__gt=30000).\
        filter(first_name__startswith='Y')
print("4. Find all full time instructors with First Name starts with `Y` and learners count greater than 30000")
print(full_time_instructors)

print("\n")
full_time_instructors = Instructor.objects.filter(full_time=True, total_learners__gt=30000,
                                                      first_name__startswith='Y')
print("5. Find all full time instructors with First Name starts with `Y` and learners count greater than 30000")
print(full_time_instructors)