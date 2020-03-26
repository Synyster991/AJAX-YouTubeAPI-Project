from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Library

def home(request):
    return render(request, 'library/home.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'


class CreateLibrary(generic.CreateView):
    model = Library
    fields = ['title']
    template_name = 'library/create_library.html'
    success_url = reverse_lazy('home')