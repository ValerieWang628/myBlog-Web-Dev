"""myOwnProj URL Configuration

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from allUsers import views as allUser_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # this means if go to slash admin, will go to the specific url 
    path('', include('myBlog.urls')),
    # if /myBlog, go to the urls.py under the myBlog, and go to the specified path in the myBlog/urls.py
    # the myBlog/ can be changed arbitrarily, it doesn't affect
    # but the myBlog.urls must match the folder name myBlog
    # otherwise it can't find
    # if want to set the myBlog page as home page, just change the myBlog/ path to empty string
    path('register/', allUser_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'allUsers/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'allUsers/logout.html'), name = 'logout'),
    path('profile/', allUser_views.profile, name = 'profile'),
    # these login logout views are class-based views
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# only in debug mode will the media root displayed after the original url