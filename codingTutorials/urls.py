"""codingTutorials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from library import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # AUTH
    path('signup', views.SignUp.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    #Library
    path('library/create', views.CreateLibrary.as_view(), name='CreateLibrary'),
    path('library/<int:pk>', views.DetailLibrary.as_view(), name='DetailLibrary'),
    # path('library/create/<int:pk>/update', views.UpdateLibrary.as_view(), name='UpdateLibrary'),
    # path('library/create/<int:pk>/delete', views.DeleteLibrary.as_view(), name='DeleteLibrary'),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
