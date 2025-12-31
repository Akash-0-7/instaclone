from django.db import models 

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    user_type=models.CharField(max_length=15)

    def __str__(self):
        return self.username
    
class User(models.Model):
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    phone=models.CharField(max_length=10)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='insta')

    def __str__(self):
        return self.firstname
    
class Post(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    image=models.ImageField(upload_to='insta')
    date_time=models.DateTimeField(auto_now=True)
    description=models.CharField(max_length=100)
    like_count=models.IntegerField(default=0)

    def __str__(self):
        return self.description
    
class Comment(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    date_time=models.DateTimeField(auto_now=True)
    comment=models.CharField(max_length=100)
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
    
class Likes(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    POST=models.ForeignKey(Post,on_delete=models.CASCADE)
    date_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date_time
    




class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_given')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_received')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
class Notification(models.Model):
    NOTIF_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # the user who triggered the notification
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_notifications')  # the user who will see the notification
    notif_type = models.CharField(max_length=10, choices=NOTIF_TYPES)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)  # optional, only for like/comment
    message = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -> {self.target_user}: {self.message}"


    
    


    
