from django.shortcuts import render,redirect
from django.contrib.auth.models import *
from django.contrib import auth,messages
from .models import *




def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']


        q1=Login.objects.filter(username=username,password=password).exists()

        if q1:
            q2=Login.objects.get(username=username,password=password)
            request.session['login_id']=q2.pk
            login_id=request.session.get('login_id')

            if q2.user_type=='admin':
                return redirect('admin')
            elif q2.user_type=='user':
                use=User.objects.get(LOGIN=login_id)
                request.session["user_id"]=use.pk
                return redirect('home')
            else :
                messages.error(request,'invalid username or password')
                return redirect("login")
        
    return render(request,'login.html')

def user(request):
    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        image=request.FILES.get('image')

        q1=Login.objects.create(username=username,password=password,user_type='user')
        q1.save()

        q2=User.objects.create(firstname=firstname,lastname=lastname,email=email,image=image,LOGIN_id=q1.pk)
        q2.save()
        return redirect('login')

    return render(request,'signup.html')

def post(request):
    return render(request,'')
def home(request):
    user_id = request.session.get('user_id')  
    all_posts = Post.objects.all().order_by('-id')  

    for post in all_posts:
        
        if user_id:
            post.is_liked = Likes.objects.filter(USER_id=user_id, POST_id=post.id).exists()

            
            post.is_following = Follow.objects.filter(follower_id=user_id, following_id=post.USER.id).exists()
        else:
            post.is_liked = False
            post.is_following = False

    return render(request, 'home.html', {'result': all_posts})







def adminhome(request):
    pos=Post.objects.all()
    return render(request,'adminhome.html',{'result':pos})

def addpost(request):
    user_id=request.session["user_id"]
    if request.method == 'POST':
        title=request.POST['title']
        description=request.POST['description']
        image=request.FILES.get('image')

        post=Post.objects.create(image=image,title=title,description=description,USER_id=user_id)
        post.save()

        return redirect('home')

    return render(request,'post.html')

def userpostview(request):
    user_id=request.session['user_id']
    po=Post.objects.filter(USER_id=user_id)
    return render(request,'userpostview.html',{'result':po})

def comment(request, id):
    user_id = request.session['user_id']
    post_id = id
    if request.method == 'POST':
        comment_text = request.POST['comment']
        
        comm = Comment.objects.create(comment=comment_text, USER_id=user_id, POST_id=post_id)
        comm.save()

        
        post = Post.objects.get(id=post_id)
        if post.USER.id != user_id:  
            Notification.objects.create(
                user=User.objects.get(id=user_id), 
                target_user=post.USER,  
                notif_type='comment',
                message=f"commented on your post: {comment_text[:50]}"  
            )

        return redirect('home')
    return render(request, 'comment.html', {'post_id': post_id})


def commentview(request,id):

    post_id=id
    pos=Comment.objects.filter(POST_id=post_id)
    return render(request,'viewcomment.html',{'result':pos,'post_id':post_id})

def delete(request,id):
    Post.objects.get(id=id).delete()
    return redirect('userpostview')

def editpost(request,id):
    old_data = Post.objects.get(id=id)
    # old_data1= User.objects.get(id=id)
    if request.method == 'POST':
        title=request.POST['title']
        description=request.POST['description']
        if 'image' in request.FILES:
               old_data.image=request.FILES.get('image')
        old_data.title=title
        old_data.description=description
        old_data.save()

        return redirect('userpostview')
        
    return render(request,'editpost.html',{'result':old_data})

def likes(request, id):
    user_id = request.session['user_id']
    post = Post.objects.get(id=id)
    user = User.objects.get(id=user_id)  #

    like = Likes.objects.filter(USER_id=user_id, POST_id=id).first()

    if like:
        
        like.delete()
        if post.like_count > 0:
            post.like_count -= 1
        post.save()
    else:
       
        Likes.objects.create(USER_id=user_id, POST_id=id)
        post.like_count += 1
        post.save()

        
        if post.USER.id != user_id:
            Notification.objects.create(
                user=user,                 
                target_user=post.USER,     
                notif_type='like',
                post=post,
                message=f"liked your post '{post.title}'"
            )

    return redirect('home')




def deleteadmin(request,id):
    Post.objects.get(id=id).delete()
    return redirect('admin')

def follow(request, id):
    user_id = request.session['user_id']
    follower = User.objects.get(id=user_id)      
    following = User.objects.get(id=id)          

    
    relation = Follow.objects.filter(follower=follower, following=following).first()

    if relation:  
       
        relation.delete()
    else:
      
        Follow.objects.create(follower=follower, following=following)

        
        if follower.id != following.id:
            Notification.objects.create(
                user=follower,             
                target_user=following,    
                notif_type='follow',
                message=f"started following you"
            )

    return redirect('home')


def unfollow(request, id):
    user_id = request.session['user_id']
    follower = User.objects.get(id=user_id)
    following = User.objects.get(id=id)

    
    relation = Follow.objects.filter(follower=follower, following=following).first()
    if relation:
        relation.delete()
        
def notification(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  

    
    notifications = Notification.objects.filter(target_user_id=user_id).order_by('-time')

    return render(request, 'notification.html', {'notifications': notifications})


    return redirect('home')




def profileedit(request,id):
        old_data1= User.objects.get(id=id)

        if request.method == 'POST':

            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            email=request.POST['email']
            phone=request.POST['phone']
            image=request.POST['image']

            old_data1=firstname=firstname
            old_data1=lastname=lastname
            old_data1=email=email
            old_data1=phone=phone
            old_data1=image=image
            old_data1.save()

            return redirect('userpostview')

        return render(request,'')
    
def profile(request, user_id):
    try:
        
        profile_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        
        return redirect('home')

    
    posts = Post.objects.filter(USER=profile_user).order_by('-id')

    
    following_list = Follow.objects.filter(follower=profile_user)

    followers_list = Follow.objects.filter(following=profile_user)

    
    logged_in_user_id = request.session.get('user_id')
    is_following = False
    if logged_in_user_id and int(logged_in_user_id) != profile_user.id:
        try:
            logged_in_user = User.objects.get(id=logged_in_user_id)
            is_following = Follow.objects.filter(
                follower=logged_in_user,
                following=profile_user
            ).exists()
        except User.DoesNotExist:
            pass  

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'followers_list': followers_list,
        'following_list': following_list,
        'followers_count': followers_list.count(),
        'following_count': following_list.count(),
        'is_following': is_following
    }

    return render(request, 'profile.html', context)



def follow_action(request, user_id):
    logged_in_user_id = request.session.get('user_id')
    if not logged_in_user_id:
        return redirect('login')
    
    logged_in_user = User.objects.get(id=logged_in_user_id)
    target_user = User.objects.get(id=user_id)
    
    relation = Follow.objects.filter(follower=logged_in_user, following=target_user).first()
    
    if relation:
        relation.delete() 
    else:
        Follow.objects.create(follower=logged_in_user, following=target_user)  
    
    return redirect('profile', user_id=user_id)








