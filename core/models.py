from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField("HeadLine", max_length=256, unique=True)
    creator = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    url = models.URLField("URL", max_length=256,blank=True)
    description = models.TextField("Description", blank=True)
    votes = models.IntegerField(null=True, default=0)
    comments = models.IntegerField(null=True)   


    ##__str__ function that shows the stuff we want to print out. This was helpful for formatting the comment tags
    def __str__(self):
        return 'Post title: {title1}, created by: {creator1}'.format(title1=self.title, creator1=self.creator) 

    ##return the number of characters, this was helpful for statistics page
    def __len__(self):
        return len(self.description)

    ##init the votes
    def count_votes(self):
        self.votes = Vote.objects.filter(post = self).count()
    

    ##count the number of comments a post has
    def count_comments(self):
        self.comments = Comment.objects.filter(post = self).count()



class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __eq__(self):
        return self.user == self.user and self.voter == self.voter
    def __str__(self):
        return f"{self.user.username} upvoted {self.link.title}" 
    def __unicode__(self):
        return f"{self.user.username} upvoted {self.link.title}" 


class Comment(models.Model):
    ##create foreign kety
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ##post foreign keyt
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ##conetn is just a textfield
    content = models.TextField()
    ##the identifier is the nesting of the comments
    identifier = models.IntegerField()
    ##foreign key to parent comment
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
    def __unicode__(self):
        return f"Comment by {self.user.username}"

