from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    # path(route='', view=views.index, name='index'),
    # path for about view
    path(route='', view=views.about, name='about'),
    # path for contact us view

    path(route='', view=views.contact, name='contact'),
    # path for registration
    path(route='', view=views.registration_request, name='register'),
    # path for login
    path(route='', view=views.login_request, name='login'),
    # path for logout
    path(route='', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view

    path(route='dealer/<int:dealer_id>/', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
