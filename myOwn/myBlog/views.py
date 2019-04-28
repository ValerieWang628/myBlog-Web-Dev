## the structure is copied from Corey Schafer's YouTube tutorials/.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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

def like_post(request):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    PostListView.liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        # liked = False
        PostListView.liked = False
    else:
        post.likes.add(request.user)
        # liked = True
        PostListView.liked = True
    return HttpResponseRedirect(post.get_absolute_url())



class PostListView(ListView):
    # this is a class that inherents from the django listview class
    model = Post 
    liked = None
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
        context['liked'] = [self.liked]
        return context




class IndividualPostView(DetailView):
    model = Post
    # automatically looks for a template named: myBlog/post_detail.html
    # if the template is already named according to the convention, no need to specify
    # the default context_object_name is 'object'
    # if the template variable is already written and don't want to change
    # specify the attribute, like what i did in the PostListView()



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
