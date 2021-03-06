from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Library, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib
import requests



YOUTUBE_API_KEY = 'AIzaSyAMabIz6N-gn3upBoAuJWWKoKER_dkR_rQ'

def home(request):
    recentLibraries = Library.objects.all().order_by('-id')[:3]
    popularLibraries = [Library.objects.get(pk=1), Library.objects.get(pk=2), Library.objects.get(pk=3)]

    passing_dict = {
        "recentLibraries": recentLibraries,
        "popularLibraries": popularLibraries
    }
    return render(request, 'library/home.html', passing_dict)


@login_required
def dashboard(request):
    libraries = Library.objects.filter(user=request.user)

    passing_dict = {
        'libraries': libraries 
    }
    return render(request, 'library/dashboard.html', passing_dict)


@login_required
def AddVideo(request, pk):
    form = VideoForm()
    searchForm = SearchForm()
    library = Library.objects.get(pk=pk)

    if not library.user == request.user: # Prevent to add video in guest library
        raise Http404
    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            video = Video()
            video.library = library
            video.url = form.cleaned_data['url']
            parsedUrl = urllib.parse.urlparse(video.url)
            videoID = urllib.parse.parse_qs(parsedUrl.query).get('v')

            if videoID:
                video.youtube_id = videoID[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ videoID[0] }&key={ YOUTUBE_API_KEY }') 
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title                
                video.save()
                return redirect('DetailLibrary', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Need to be a valid YouTube URL')

    return render(request, 'library/AddVideo.html', {'form': form, 'searchForm': searchForm, 'library':library})


@login_required
def videoSearch(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({'error':'Not able to validate form'})

    
class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'library/DeleteVideo.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.library.user == self.request.user:
            raise Http404
        else:
            return video


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return view


class CreateLibrary(LoginRequiredMixin, generic.CreateView):
    model = Library
    fields = ['title']
    template_name = 'library/CreateLibrary.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateLibrary, self).form_valid(form)

        return redirect('dashboard')


class DetailLibrary(generic.DetailView):
    model = Library
    template_name = 'library/DetailLibrary.html'


class UpdateLibrary(LoginRequiredMixin, generic.UpdateView):
    model = Library
    template_name = 'library/UpdateLibrary.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        library = super(UpdateLibrary, self).get_object()
        if not library.user == self.request.user:
            raise Http404
        else:
            return library


class DeleteLibrary(LoginRequiredMixin, generic.DeleteView):
    model = Library
    template_name = 'library/DeleteLibrary.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        library = super(DeleteLibrary, self).get_object()
        if not library.user == self.request.user:
            raise Http404
        else:
            return library


