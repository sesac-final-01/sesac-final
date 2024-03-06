from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='sign-up'),
    path('signin/', views.UserSigninView.as_view(), name='sign-in'),
    path('signout/', views.UserSignoutView.as_view(), name='sign-out'),
]
