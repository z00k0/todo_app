from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .forms import RegisterForm, LoginForm
from django.views.generic import CreateView


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('projects:projects')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')


class LoginView(LoginView):
    # form_class = LoginForm
    authentication_form = LoginForm
    template_name = 'users/login.html'

    # def geet(self, request):
    #     form = self.get_form_class()
    #     return render(request, self.template_name, form)

    # def post(self, request):
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     user = authenticate(request, email=email, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return HttpResponseRedirect('projects:projects')
    #     else:
    #         return HttpResponseRedirect('users:login')
