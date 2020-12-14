from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from .models import Post,Vote,Comment
from .forms import CommentForm,PostForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Layout

from collections import defaultdict

from datetime import datetime, timezone
# Create your views here.
def StatisticsView(req):
    ##get all the models
    users = User.objects.all()
    posts = Post.objects.all()
    ##default dictionary for popular posts and for the users
    userPost = defaultdict(int, {user.username: 0 for user in users})
    popPosts = defaultdict(int)
    current_time = datetime.now(timezone.utc)
    ##get the times from the posts
    times = []
    for user in users:
        userTime = user.last_login
        hoursSinceLoggedIn = (current_time - user.last_login).total_seconds() / 3600
        times.append(hoursSinceLoggedIn)
        for post in posts:
            if (user.username == post.creator.username):
                userPost[user.username] += 1
    ##count the total ammount of votes
    totalVotes = 0
    for post in posts:
        print("This len", len(post))
        post.count_votes()
        popPosts[post] += post.votes
    

    x_data = []##[user.username for user in users]
    y_data = []##[1 for x in x_data]
    ##grab the contributions and key of name from the userposts ityems set
    for key, value in userPost.items():
        x_data.append(key)
        y_data.append(value)
    ##plot the graphs 
    plot_div1 = plot({"data":[Bar(x=x_data, y=y_data,
                     name='test',
                        opacity=0.8, marker_color='green')], "layout":Layout(title="Top user contributions", yaxis={"title":"# of posts"})},
               output_type='div')

    plot_div2 = plot({"data":[Bar(x=x_data, y=times,
                    name='test',
                    opacity=0.8, marker_color='Blue')], "layout":Layout(title="Hours since users logged in", yaxis={"title":"hours"})},
            output_type='div')
    #for the posts grab the data from that
    l1 = []
    l2 = []
    l3 = []
    l4 = []
    for key,value in popPosts.items():
        l3.append((key.title, value))
        l4.append((key.title, len(key)))
    ##sort #of good questions and length of description in descending order
    l3.sort(key=lambda x:x[1], reverse=True)
    l4.sort(key=lambda x:x[1], reverse=True)
    l1 = (x for (x,y) in l3)
    l2 = (y for (x,y) in l3)
    l1 = list(l1)
    l2 = list(l2)
    plot_div3 = plot({"data":[Scatter(x=list(l1), y=list(l2),
                name='test',
                opacity=0.8, marker_color='Yellow')], "layout":Layout(title="Popular posts", yaxis={"title":"# of good questions"})},
        output_type='div')
    l1 = (x for (x,y) in l4)
    l2 = (y for (x,y) in l4)
    l1 = list(l1)
    l2 = list(l2)
    plot_div4 = plot({"data":[Scatter(x=list(l1), y=list(l2),
        name='test',
        opacity=0.8, marker_color='Brown')], "layout":Layout(title="Longest posts", yaxis={"title":"Length of description in characters"})},
        output_type='div')
    return render(req, '../../Piazza/templates/statistics.html', context={'plot_div1': plot_div1, 'plot_div2':plot_div2, 'plot_div3':plot_div3, 'plot_div4':plot_div4})

def PostListView(request):
    ##show all the posts
    posts = Post.objects.all()
    for post in posts:
        post.count_votes()
        post.count_comments()
        
    context = {
        'posts': posts,
    }
    return render(request,'../../Piazza/templates/postlist.html',context)

from datetime import datetime,timedelta
from django.utils import timezone

def NewPostListView(request):
    ##order the posts based on the time they were created
    posts = Post.objects.all().order_by('-created_on')
    for post in posts:
        post.count_votes()
        post.count_comments()    
    context = {
        'posts': posts,
    }
    return render(request,'../../Piazza/templates/postlist.html', context)


def PastPostListView(request):
    ##sort the posts by the time
    time = str((datetime.now(tz=timezone.utc) - timedelta(minutes=1)))
    ##only show posts older than one minute ago
    posts = Post.objects.filter(created_on__lte = time)
    for post in posts:
        post.count_votes()
        post.count_comments()

    context={
        'posts': posts,
    }
    return render(request,'../../Piazza/templates/postlist.html',context)

def UpVoteView(request,id):
    if request.user.is_authenticated:
        ##only allow voting for authed users
        post = Post.objects.get(id=id)
        votes = Vote.objects.filter(post = post)
        v = votes.filter(voter = request.user)
        ##if len is zero, make sure that you save the upvote appriatley, since there doesnt exists a vote model in table
        if len(v) == 0:
            upvote = Vote(voter=request.user,post=post)
            upvote.save()
            return redirect('/')
    return redirect('/signin')


def DownVoteView(request,id):
    ##down vote the question, but only if the user is authenticated
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        votes = Vote.objects.filter(post = post)
        ##filter based on what they have already voted on
        v = votes.filter(voter = request.user)
        if len(v) != 0:
            v.delete()
            return redirect('/')
    return redirect('/signin')    


def UserInfoView(request,username):
    ##get the user object from the currently logged in users and render it
    user = User.objects.get(username=username)
    context = {'user':user,}
    return render(request,'../../Piazza/templates/user_info.html',context)


def UserSubmissions(request,username):
    ##get the user submissions and posts
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creator = user)
    ##the len of the posts is how many characters
    print(len(posts))
    for post in posts:
        post.count_votes()
        post.count_comments()    
    return render(request,'../../Piazza/templates/user_post.html',{'posts': posts})
  
def EditListView(request,id):
    ##if there is no post yield a 404 error
    post = get_object_or_404(Post,id=id)
    ##check if the method is piost
    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    ##instantiate the form as a post form from django and send that form to be rendered in the html
    form = PostForm(instance =post)
    return render(request,'../../Piazza/templates/submit.html',{'form':form})


def CommentListView(request,id):
    ##get the necessary variables
    form = CommentForm()
    post = Post.objects.get(id =id)
    post.count_votes()
    post.count_comments()

    comments = [] 
    ##creat a function to check which level the comment should be nestyed in    
    def func(i,parent):
        children = Comment.objects.filter(post =post).filter(identifier =i).filter(parent=parent)
        for child in children:
            gchildren = Comment.objects.filter(post =post).filter(identifier = i+1).filter(parent=child)
            if len(gchildren)==0:
                comments.append(child)
            else:
                func(i+1,child)
                comments.append(child)
    func(0,None)
    print(comments)
    ##only if the method is post should we check the cvomments
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                comment = Comment(creator = request.user,post = post,content = content,identifier =0)
                comment.save()
                return redirect(f'/post/{id}')
        return redirect('/signin')
    
    ##send the context to the html
    context ={
        'form': form,
        'post': post,
        'comments': list(reversed(comments)),
    }
    return render(request,'../../Piazza/templates/commentpost.html', context)


def CommentReplyView(request,id1,id2):
    form = CommentForm()
    comment = Comment.objects.get(id = id2)
    post = Post.objects.get(id=id1)
    ##only if the method is post
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            
            if form.is_valid():
                reply_comment_content = form.cleaned_data['content']
                ##increase level of the comment in the thread
                identifier = int(comment.identifier + 1)

                reply_comment = Comment(creator = request.user, post = post, content = reply_comment_content, parent=comment, identifier= identifier)
                reply_comment.save()

                return redirect(f'/post/{id1}')
        return redirect('/signin')
    ##sned the conntext of the comment into the html templlate
    context ={
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request,'../../Piazza/templates/reply_post.html', context)

def SubmitPostView(request):
    if request.user.is_authenticated:
        ##only post if user is authenticated
        form = PostForm()

        if request.method == "POST":
            form = PostForm(request.POST)
            ##check if the form is valid
            if form.is_valid():
                title = form.cleaned_data['title']
                url = form.cleaned_data['url']
                description = form.cleaned_data['description']
                creator = request.user
                created_on = datetime.now()

                post = Post(title=title, url=url, description=description, creator = creator, created_on=created_on)

                post.save()
                return redirect('/')
        return render(request,'../../Piazza/templates/submit.html',{'form':form})
    return redirect('/signin')

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

def signup(request):
    #logic for the sign up
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('/')
        
        else:
            return render(request,'../../Piazza/templates/auth_signup.html',{'form':form})
    
    else:
        form = UserCreationForm()
        return render(request,'../../Piazza/templates/auth_signup.html',{'form':form})


def signin(request):
    ##logic for the sign in page
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request,'../../Piazza/templates/auth_signin.html',{'form':form})
    
    else:
        form = AuthenticationForm()
        return render(request, '../../Piazza/templates/auth_signin.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('/')