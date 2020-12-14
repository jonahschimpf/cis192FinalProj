###Code structure
The code structure follows the template from lecture which is MVT: Or model, view template.
First, there are models for Votes, Posts, Users, and Comments. The idea is that the comments 
and votes and posts  need to store the user who made the preceding as foreign keys. This makes
sense, since we are definetly not only interested what the object in the web app are
but who made the objects in our web app. Next, we also include the ability to get the link from the top of
the question, just like real piazza and we have the ability to check out and edit a question (if we are a user)
by the methods outlined in lecture. Particularlly, I am conditionally rendering the edit button depending on if 
the question that is relevant was authored by the currently logged in user. I also make use of plotly
to display releveant statistics about the users. This includes the time model. 
 Outlined below are the MVT structure:
Templates:
auth_signin-->default sign in page from django
auth_signup-->default sign up page from django
base->the base html that all of them follow for bootstrap
comment_post->>html which represents comment
poslist->main feed
reply_post->the html which shows what replying should look like
statistic-> relevant statistics about the users using plotly and datetime
submit->submit form for a question
user-info->dedicated user page
user_post->dedicateduser_posting page

Views
 
 The views mirror the same idea in lecture, which templates having essentially one view per. I implemented much of the backend logic
 here and made sure to be careful about allowing only authenticated users to access the logic of the website. Moreover, I also impolemented
 nesting comments, statistics, upvoting, editing, submitting, loggin in and signing up here.

 Models:

 I just have 4 models:
User, Comment, Vote, Post
The comment vote and post have foreign key references to user. And both the Vote and Comment have foreign key references
to post, since the aformentioned cannot exist without a post!. I chose this method of implementation to abstract away the details of 
keeping track of posts, votes, and comments manually, and instead relied on the backend to update the state of the program appropriately. 

Description:
Welcome to a piazza clone! Inspired by my obsession with piazza feel free to make questions, 'good question' and 'bad question' mark questions and 
edit your posts. Also, check out the statistics page, which has realtime statistics about the current user sessions. 


Requirements met:
One class definition (with at least two magic methods)
-> I have three class definitions. The Post class implements __str__ which returns a well formated string of the post 
and __len__ which returns  the length of the post (# of characters). I use both for the statistics page

Two non-trivial first-party packages (e.g. json, time)
-> I use defaultdict throughout the program and I also use datetime and timestamp to order the older post and display relevant statistics regarding time

Two non-trivial third-party packages (e.g. Django, Tensorflow/Keras)
-> Django for the webapp portion and plotly to display the statistics
In-line documentation (i.e. comments in code)

-> I have comment throughout! Enjoy :)

Installation instruction
---> I think you just do pip requriements and run the server using django! If there are any installation errors please let me know!
Im new to python so I'm not super sure how this works.