from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# the post model and user model are going to have a relationship
from django.urls import reverse

class Post(models.Model):
    # each class is going to be own table and database
    # each attribute of it will be a diff. field in the database
    subject = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name = 'likes', blank = True)
    favorites = models.ManyToManyField(User, related_name = 'favorites', blank = True)
    # foreignKey: one to many relation
    # on_delete specifies what to do if a user is deleted

    def __str__(self):
        return self.subject 
        
    
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('individual-post', kwargs = {'pk':self.pk})
        # this is to get the individual post url and add the interger pk to it
        # so that creating a new post won't direct to a 404
        # kwargs is a dict, the 'pk' serves as a url key here; self.pk is the value


