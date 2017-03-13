from popilicity.models import Location
from rest_framework import routers, serializers, viewsets
from api.user import UserSerializer

# Serializers define the API representation.
class LocationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:location-detail")
    class Meta:
        model = Location
        fields = ('url', 'name')

    def create(self, validated_data):
        post, created =  Location.objects.get_or_create(**validated_data)
        return post


# ViewSets define the view behavior.
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
