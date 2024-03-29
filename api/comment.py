from popilicity.models import Comment
from rest_framework import routers, serializers, viewsets
from api.user import UserSerializer
import autoActions


# Serializers define the API representation.
class CommentSerializer(serializers.ModelSerializer):
    url   = serializers.HyperlinkedIdentityField(view_name="api:comment-detail")
    owner = UserSerializer(read_only=True)
    post_url  =  serializers.HyperlinkedIdentityField(view_name="api:post-detail")

    class Meta:
        model = Comment
        fields = ('id', 'url', 'post_url', 'owner', 'text', 'create_date')
        write_only_fields = ('post_id',)

    def create(self, validated_data):
        post_id = self.initial_data['post_id']
        comment = Comment(owner_id=self.context['request'].user.id, post_id=post_id, **validated_data)
        comment.save()
        user = self.context['request'].user
        autoActions.newComment(post_id, user)
        return comment

# ViewSets define the view behavior.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('text',)
