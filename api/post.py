from popilicity.models import Post
from rest_framework import routers, serializers, viewsets
from api.user import UserSerializer
from api.location import LocationSerializer
from api.interest import InterestSerializer
from api.comment import CommentSerializer


# Serializers define the API representation.
class PostSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.HyperlinkedIdentityField(view_name="api:user-detail")
    owner = UserSerializer(read_only=True)
    location = LocationSerializer()
    interest = InterestSerializer()
    comment_set = CommentSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedIdentityField(view_name="api:post-detail")
    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'type',
            'owner',
            'path',
            'location',
            'interest',
            'comment_set',
            'status',
            'create_date',
            'update_date',
        )


# ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
