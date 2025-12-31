from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.login,name='login'),
    path('signup',views.user,name='signup'),
    path('home',views.home,name='home'),
    path('admin',views.adminhome,name='admin'),
    path('post',views.post,name='post'),
    path('addpost',views.addpost,name='addpost'),
    path('userpostview',views.userpostview,name='userpostview'),
    path('comment/<int:id>',views.comment,name='comment'),
    path('commentview/<int:id>',views.commentview,name='commentview'),
    path('deletepost/<int:id>',views.delete,name='deletepost'),
    path('editpost/<int:id>',views.editpost,name='editpost'),
    path('like/<int:id>',views.likes,name='like'),
    path('deleteadmin<int:id>',views.deleteadmin,name='deleteadmin'),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('notification',views.notification,name='notification'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow_action, name='follow_action'),
    

    
    
]