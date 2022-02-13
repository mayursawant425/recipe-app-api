from django.urls import path

from User import views


app_name = 'User'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.AuthTokenView.as_view(), name='token'),
]
