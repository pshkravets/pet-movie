from django.urls import path, include

from .views import SignUpView, LoginView, logout_view, AccountActivateView, send_otp_view

urlpatterns = [
    path('signup', SignUpView.as_view(), name='authorization'),
    path('activate', AccountActivateView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name='login_user'),
    path('logout', logout_view, name='logout'),
    path('send_otp', send_otp_view, name='send_otp'),
    path('social-auth', include('social_django.urls', namespace='social'))

]