from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from . import forms

# Create your views here.

class SignupView(generic.CreateView):
    form_class = forms.SignupForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
