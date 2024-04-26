from django.urls import path, re_path
from django.views.generic import RedirectView, TemplateView
from faculty.views import register_view, login_view, logout_view, profile_view, join_classroom, classroom_view

app_name = 'faculty'

urlpatterns = [
    path("", TemplateView.as_view(template_name="faculty/home.html"), name="home"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('join_classroom/<int:classroom_id>', join_classroom, name='join_classroom'),
    path('classroom/<int:classroom_id>/', classroom_view, name='classroom_view'),
    re_path(r'^.*$', RedirectView.as_view(pattern_name='faculty:home')),
]


