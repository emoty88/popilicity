from popilicity.models import Interest
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class InterestSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:interest-detail")
    class Meta:
        model = Interest
        fields = ('id', 'url', 'name')

    def create(self, validated_data):
        interest, created =  Interest.objects.get_or_create(**validated_data)
        return interest


# ViewSets define the view behavior.
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
