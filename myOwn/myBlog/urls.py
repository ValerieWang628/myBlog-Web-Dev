# Cited from Corey Schafer
from django.urls import path
from . import views

from .views import PostListView, IndividualPostView, CreatePostView, EditPostView, DeletePostView
# this is to directly import the listView class into the urls.py

urlpatterns = [
    path('post/<int:pk>/', IndividualPostView.as_view(), name = 'individual-post'),
    # pk stands for primary key, it will generate the path with the corresponding key
    # int: means only put the interger of primary keys, not strings
    # pk also matched naming conventions

    path('post/<int:pk>/edit/', EditPostView.as_view(), name = 'individual-post-update'),

    path('post/<int:pk>/delete/', DeletePostView.as_view(), name = 'individual-post-delete'),

    path('post/<int:pk>/favorites/', views.favorite_post, name = 'favorite-post'),

    path('post/likes/', views.like_post, name = 'like-post'),

    # path('post/favorites/', views.favorite_post, name = 'favorite-post'),

    path('post/new/', CreatePostView.as_view(), name = 'new-post'),
    # this will look for a file for post_form.html

    path('', PostListView.as_view(), name = 'myBlogHome'),
    # this is to directly use the class-based view
    # to access the actual view, have to use a built-in method, as_view()

    # path('', views.home, name = 'myBlogHome'),
        # empty path means the very default page
        # the views.home means to direct to the home function of view.py
        # the home function is in the view.py to display the post content into the html template
    path('about/', views.about, name = 'myBlogAbout'),
    path('search/', views.search, name = 'searchPage'),
    path('smartsearch/', views.smartSearch, name = 'smartSearch'),
    # need a trailing slash
    # don't need to update in the myOwnProj urls.py 
    # because the main urls.py sends anything of blog to myBlog and lets myBlog handles that
] 

# the url pattern is actually looking for a file to display,
# due to the django builtin convention, the file is named as
# <app>/<model>_<viewtype>.html
# eg: if passing PostListView.as_view(), should be: myBlog/post_list.html
# I can either change the template name to match this naming convention
# or I can change the route of what urlpattern is looking for