from popilicity.models import Post, Reaction, Profile

def postReaction(post_id, reaction, oldReaction):
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
