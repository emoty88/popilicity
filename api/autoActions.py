from popilicity.models import Post, Reaction, Profile, Notification
from django.db.models import Sum
import datetime

def postReaction(post_id, reaction, oldReaction, user):
    post = Post.objects.get(pk=post_id)
    point = 0
    addLike = 0
    addDisLike = 0
    if oldReaction:
        if oldReaction == reaction:
            return False
        else:
            if reaction == 1:
                point = 3.7
                addLike = 1
                addDisLike = -1
            else:
                point = -3.7
                addLike = -1
                addDisLike = 1
    else:
        addNotification(user, post.owner, post, reaction)
        if reaction == 1:
            point = 4
            addLike = 1
        else:
            point = 0.3
            addDisLike = 1

    post.point = post.point + point
    post.save()

    profile = Profile.objects.filter(user=post.owner).first()

    # print addLike
    # print addDisLike
    # print profile.like_count
    # print profile.dislike_count

    profile.like_count = profile.like_count + addLike
    profile.dislike_count = profile.like_count + addDisLike
    profile.save()
    return True

def newPost(post):
    profile = Profile.objects.filter(user=post.owner).first()
    profile.post_count = profile.post_count + 1
    profile.save()
    return True

def newComment(post_id):
    post = Post.objects.get(pk=post_id)
    post.point = post.point + 2
    post.save()
    return True

def userPointCalculate(user_id):
    user_point = 0
    profile = Profile.objects.filter(user_id=user_id).first()
    # last 30 hours
    end_date =  datetime.datetime.now()
    start_date = datetime.datetime.now() + datetime.timedelta(seconds=-108000)
    post_point = Post.objects.filter(owner=profile.user).filter(create_date__range=(start_date, end_date)).aggregate(Sum('point'))
    if post_point['point__sum'] is not None:
        user_point += post_point['point__sum'] * 0.1


    # between 30 hours and 180 hours
    end_date =  datetime.datetime.now() + datetime.timedelta(seconds=-108000)
    start_date = datetime.datetime.now() + datetime.timedelta(seconds=-648000)
    post_point = Post.objects.filter(owner=profile.user).filter(create_date__range=(start_date, end_date)).aggregate(Sum('point'))
    if post_point['point__sum'] is not None:
        user_point += post_point['point__sum'] * 0.07


    # older than 180 hours
    start_date = datetime.datetime.now() + datetime.timedelta(seconds=-648000)
    post_point = Post.objects.filter(owner=profile.user).filter(create_date__lt=start_date).aggregate(Sum('point'))
    if post_point['point__sum'] is not None:
        user_point += post_point['point__sum'] * 0.012

    profile.point = user_point
    profile.save()
    return True

def addNotification(owner, target_usr, target_post, action):
    noti = Notification(owner_id=owner.id)
    noti.target_usr = target_usr
    noti.target_post = target_post
    noti.action = action
    noti.save()
    return True
