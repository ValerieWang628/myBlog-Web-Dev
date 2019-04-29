## the structure is copied from Corey Schafer's YouTube tutorials/.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, F, Count


# def home(request):

#     context = {
#         'posts': Post.objects.all(),
#         'title': 'home',
#     }
#     return render(request, 'myBlog/index.html', context)
    # return HttpResponse('<h1>The xxx Page</h1>')
    # this function is: the home page gets all the post objects and put them into the html file and present them

def about(request):
    return render(request, 'myBlog/about.html', {'title': 'about'})

def search(request):
    queryPool = Post.objects.all()
    query = request.GET.get("q")
    queryDictionary = request.GET
    # https://docs.djangoproject.com/en/1.8/topics/db/aggregation/#order-by
    # https://github.com/codingforentrepreneurs/try-django-19/blob/master/src/posts/views.py
    if query:
        query_result = queryPool.filter(
                Q(subject__icontains=query)|
                Q(content__icontains=query)|
                Q(date_posted__icontains=query) |
                Q(author__username__icontains=query)
                ).annotate(like_nums = Count('likes')).distinct().order_by('-like_nums','-date_posted') 
                # distinct is to remove duplicate rows
    else: query_result = queryPool

    if 'search_fav' in queryDictionary:
        query_fav = True
    else: query_fav = False

    fav_dict = dict()
    for po in query_result:
        if request.user in po.favorites.all():
            fav_dict[po] = True
        else: fav_dict[po] = False

    like_num_dict = dict()
    for po in query_result:
        like_num_dict[po] = len(po.likes.all())

    context = {
        'posts': query_result,
        'like_num': like_num_dict,
        'fav_status': fav_dict,
        'query_type': query_fav,
    }
    
    return render(request, 'myBlog/search.html', context)

def like_post(request):
    post = get_object_or_404(Post, id = request.POST.get('like'))
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

def favorite_post(request, pk):
    post = get_object_or_404(Post, id = request.POST['favorite'])
    if post.favorites.filter(id = request.user.id).exists():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

class PostListView(ListView):
    # this is a class that inherents from the django listview class
    model = Post 
    posts = Post.objects.all()
    # to specify what model to use, and what data to get from
    # in this case, it will fetch the subject, content, data_posted, author data of this class object
    # I already created the post model, a model class inherent from the builtin model class
    # to make the template match the naming convention: <app>/<model>_<viewtype>.html
    template_name = 'myBlog/index.html'
    context_object_name = 'posts'
    # this contect_object_name is to pass the Post model data into the 'posts' variable in the index.html template
    # these three parameters are specifying what model to use data from; what template to use; and match the variable in the template
    ordering = ['-date_posted']
    # this is from latest to oldest, to reverse, remove the minus sign

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_status'] = self.liked_status()
        context['like_num'] = self.how_many_likes()
        return context

    
    def liked_status(self):
        liked = set()
        for po in PostListView.posts:
            if self.request.user in po.likes.all():
                liked.add(po)
        return liked
    
    def how_many_likes(self):
        like_num_dict = dict()
        for po in PostListView.posts:
            like_num_dict[po] = len(po.likes.all())
        return like_num_dict


class IndividualPostView(DetailView):
    model = Post
    posts = Post.objects.all()
    # automatically looks for a template named: myBlog/post_detail.html
    # if the template is already named according to the convention, no need to specify
    # the default context_object_name is 'object'
    # if the template variable is already written and don't want to change
    # specify the attribute, like what i did in the PostListView()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorited_status'] = self.favorited_status()
        return context

    def favorited_status(self):
        favorited = set()
        for po in IndividualPostView.posts:
            if self.request.user in po.favorites.all():
                favorited.add(po)
        return favorited

class CreatePostView(LoginRequiredMixin, CreateView):
    # should provide fields 
    # date will be automatically filled in
    model = Post
    fields = ['subject', 'content']
    # if simply submit like that, there will be an integrity error because every post has to have an author
    # this was determined by the model
    # an author can have multiple posts but a post must have one author
    # need to specify the author field, and connect it to the current logged in user
    def form_valid(self, form):
        '''this is to override the pre-builtin form valid method'''
        form.instance.author = self.request.user
        # to set the author as the current logged-in user
        return super().form_valid(form)
        # after setting the author, make this method functions as the regular parent form_valid method
    
    # after that, should create a redirect url for the new post. 
    
class EditPostView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['subject', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return ((self.request.user == post.author))

class DeletePostView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Post
    success_url = '/'
    # if a post is deleted, need to specify where the after-deletion-session should redirect

    def test_func(self):
        post = self.get_object()
        return ((self.request.user == post.author))



# fakePosts = [
# {
#     'author': 'Valerie Wang',
#     'subject': 'I love Jazz',
#     'content': 'I think Jazz is the best',
#     'date_posted': 'April 20, 2018'
# },
# {
#     'author': 'Hao Wu',
#     'subject': 'Pop is better',
#     'content': 'I think pop music is the best',
#     'date_posted': 'April 21, 2018'
# },
# {
#     'author': 'Kuangji Shen',
#     'subject': 'You both are dumb',
#     'content': 'I think they both sucks',
#     'date_posted': 'April 22, 2018'
# }
# ]
