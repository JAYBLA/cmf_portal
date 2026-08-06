from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

from .forms import LoginForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        if self.request.user.role == self.request.user.Roles.EMPLOYEE:
            return reverse("dashboard:dashboard")
        return super().get_success_url()


class UserLogoutView(LogoutView):
    next_page = "users:login"
