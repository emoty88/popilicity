from popilicity.models import Comment
from rest_framework import routers, serializers, viewsets
from api.user import UserSerializer
from api.location import LocationSerializer
from api.interest import InterestSerializer


# Serializers define the API representation.
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url   = serializers.HyperlinkedIdentityField(view_name="api:comment-detail")
    owner = UserSerializer(read_only=True)
    post_url  =  serializers.HyperlinkedIdentityField(view_name="api:post-detail")
    class Meta:
        model = Comment
        fields = ('url', 'post_url', 'owner', 'text')

# ViewSets define the view behavior.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
