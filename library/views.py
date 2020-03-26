from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Library


def home(request):
    return render(request, 'library/home.html')

def dashboard(request):
    return render(request, 'library/dashboard.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return view

class CreateLibrary(generic.CreateView):
    model = Library
    fields = ['title']
    template_name = 'library/CreateLibrary.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateLibrary, self).form_valid(form)

        return redirect('home')


class DetailLibrary(generic.DetailView):
    model = Library
    template_name = 'library/DetailLibrary.html'


class UpdateLibrary(generic.UpdateView):
    model = Library
    template_name = 'library/UpdateLibrary.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')


class DeleteLibrary(generic.DeleteView):
    model = Library
    template_name = 'library/DeleteLibrary.html'
    success_url = reverse_lazy('dashboard')


