from popilicity.models import Profile
from rest_framework import routers, serializers, viewsets
from api.Base64ImageField import Base64ImageField
from api.location import LocationSerializer
from api.interest import InterestSerializer
from api.user import UserSerializer



# Serializers define the API representation.
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    location = LocationSerializer()
    interest = InterestSerializer()
    image = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
        model = Profile
        fields = ('id', 'image', 'user', 'location', 'interest')

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
        print profile
        profile.save()
        return profile

# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
