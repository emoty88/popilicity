from popilicity.models import Post
from rest_framework import routers, serializers, viewsets
from api.Base64ImageField import Base64ImageField
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
    path = serializers.ImageField(
            max_length = None, use_url=True
        )

    url = serializers.HyperlinkedIdentityField(view_name="api:post-detail")
    path = Base64ImageField(max_length=None, use_url=True,)

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

    def create(self, validated_data):
        print self.context['request'].user
        print 'post serializer create method'
        location = validated_data.pop('location')
        locationObj = LocationSerializer(data=location)
        if locationObj.is_valid():
            locationIns = locationObj.save()
        else:
            print locationObj.errors

        interest = validated_data.pop('interest')
        interestObj = InterestSerializer(data=interest)
        if interestObj.is_valid():
            interstIns = interestObj.save()
        else:
            print interestObj.errors

        post = Post(owner_id=self.context['request'].user.id, location=locationIns, interest=interstIns,  **validated_data)
        post.save()
        return post


# ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
