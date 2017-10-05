from popilicity.models import Profile
from rest_framework import routers, serializers, viewsets, filters
from api.Base64ImageField import Base64ImageField
from api.location import LocationSerializer
from api.interest import InterestSerializer
from api.user import UserSerializer
import django_filters



# Serializers define the API representation.
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    location = LocationSerializer()
    interest = InterestSerializer()
    image = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
        model = Profile
        fields = ('id', 'image', 'user', 'location', 'interest', 'post_count', 'like_count', 'dislike_count', 'point')

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

        profile = Profile(user=self.context['request'].user, location=locationIns, interest=interstIns, **validated_data)
        # print profile
        profile.save()
        return profile

    def update(self,instance, validated_data):
        location = validated_data.pop('location')
        locationObj = LocationSerializer(data=location)
        if locationObj.is_valid():
            locationIns = locationObj.save()
        else:
            print locationObj.errors
        instance.location = locationIns

        interest = validated_data.pop('interest')
        interestObj = InterestSerializer(data=interest)
        if interestObj.is_valid():
            interstIns = interestObj.save()
        else:
            print interestObj.errors
        instance.interest = interstIns
        if 'image' in validated_data:
            instance.image = validated_data['image']
        instance.save()
        return instance

class ProfileFilter(django_filters.FilterSet):
    user__name__contains = django_filters.CharFilter(name="user__first_name", lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = (
            'user',
            'user__first_name',
            'user__name__contains',
            'interest__name'
            )

# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = ProfileFilter
    ordering_fields = ('point', 'id')
