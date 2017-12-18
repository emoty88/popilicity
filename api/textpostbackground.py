from popilicity.models import TextPostBackground
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class TextPostBackgroundSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TextPostBackground
        fields = ('id', 'path', 'name')

    def create(self, validated_data):
        background, created =  TextPostBackground.objects.get_or_create(**validated_data)
        return background



# ViewSets define the view behavior.
class TextPostBackgroundViewSet(viewsets.ModelViewSet):
    queryset = TextPostBackground.objects.all()
    serializer_class = TextPostBackgroundSerializer
