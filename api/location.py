from popilicity.models import Location
from rest_framework import routers, serializers, viewsets
from api.user import UserSerializer

# Serializers define the API representation.
class LocationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:location-detail")
    class Meta:
        model = Location
        fields = ('url', 'name')

    # def create(self, validated_data):
    #     #return Snippet.objects.create(**validated_data)
    #     # call set_password on user object. Without this
    #     # the password will be stored in plain text.
    #     # print validated_data
    #     post = Post(**validated_data)
    #     print owner
    #     post.save()
    #     return post


# ViewSets define the view behavior.
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
