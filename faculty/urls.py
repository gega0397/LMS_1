from django.urls import path, re_path
from django.views.generic import RedirectView

from faculty.views import register #, login, profile

app_name = 'faculty'

urlpatterns = [
    path('register/', register, name='register'),
    # path('login/', login, name='login'),
    # path('profile/', profile, name='profile'),
    # re_path(r'^.*$', RedirectView.as_view(pattern_name='faculty:login')),
]