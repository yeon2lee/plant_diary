from django.urls import path
from .views import *

app_name = 'user'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('register/', register_view, name="signup"),
    path('profile/update/', profile_update, name="update"),
    path('profile/delete', profile_delete, name="delete"),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('<int:pk>/follow/', follow, name='follow'),
]