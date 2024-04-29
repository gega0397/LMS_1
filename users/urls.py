from django.urls import path, re_path
from django.views.generic import RedirectView, TemplateView
from users.views import register_view, login_view, logout_view

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]
