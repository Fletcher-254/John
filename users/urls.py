from django.urls import path
from .views import (
    RegisterUserView,
    LoginView,
    MeView,
    UserListView,
    UserUpdateView
)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:user_id>/', UserUpdateView.as_view(), name='user-update'),
]