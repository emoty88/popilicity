from popilicity.models import Post, Reaction
from rest_framework import routers, serializers, viewsets, filters
#from api.Base64ImageField import Base64ImageField
from drf_extra_fields.fields import Base64ImageField
from api.user import UserSerializer
from api.location import LocationSerializer
from api.interest import InterestSerializer
from api.comment import CommentSerializer
#import django_filters.rest_framework
from rest_framework import generics
from api.customPagination import CustomPageNumberPagination
import autoActions
import django_filters

# Serializers define the API representation.
class PostSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.HyperlinkedIdentityField(view_name="api:user-detail")
    url = serializers.HyperlinkedIdentityField(view_name="api:post-detail")
    owner = UserSerializer(read_only=True)
    location = LocationSerializer()
    interest = InterestSerializer()
    comment_set = CommentSerializer(many=True, read_only=True)

    path = Base64ImageField()
    my_reaction = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = (
            'id',
            'url',
            'type',
            'owner',
            'path',
            'location',
            'interest',
            'my_reaction',
            'comment_set',
            'status',
            'point',
            'create_date',
            'update_date',
        )


    def create(self, validated_data):
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

        first_comment = self.initial_data['comment']
        commentObj = CommentSerializer(data={'text':first_comment, 'post_id':post.id})
        commentObj.context['request'] = self.context['request']
        if commentObj.is_valid():
            commentIns = commentObj.save()
        else:
            print interestObj.errors

        autoActions.newPost(post)
        autoActions.userPointCalculate(post.owner_id)
        return post


    def get_my_reaction(self, obj):
        reaction = Reaction.objects.filter(post_id= obj.id, user_id= self.context['request'].user.id)
        if len(reaction) == 0:
            my_reaction = 0
        else :
            my_reaction = reaction[0].type

        return my_reaction

class PostFilter(django_filters.FilterSet):
    min_create_date = django_filters.DateTimeFilter(name="create_date", lookup_expr='gte')
    max_create_date = django_filters.DateTimeFilter(name="create_date", lookup_expr='lte')
    class Meta:
        model = Post
        fields = [
            'owner',
            'interest__name',
            'location__name',
            'min_create_date',
            'max_create_date',
            'create_date',
            'point']


# ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    serializer_class = PostSerializer
    filter_class = PostFilter
    ordering_fields = ('point', 'id', 'create_date')
