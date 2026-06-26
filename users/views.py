from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import LoginForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = "login"