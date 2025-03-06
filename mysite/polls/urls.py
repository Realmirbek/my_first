from django.urls import path
from .views import (UserRegistrationView, MyTokenObtainPairView, PasswordResetRequestView, PasswordSetView,
                    UserDeleteView, UserListView, UserDetailView
                    )

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('set-new-password/', PasswordSetView.as_view(), name='set-new-password'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('delete-user/<int:id>/', UserDeleteView.as_view(), name='delete-user'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

]



