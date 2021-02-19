from django.urls import path, include

from . import views

app_name = 'magic_link'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('get_login_url/', views.create_magic_link_view, name='create_magic_link'),
    path('handle_login_url/', views.handle_magic_link_view, name='handle_magic_link'),
    path('some_protected_url/', views.protected_url_view, name='protected_url'),
    path('', views.home_view, name='home'),
]
