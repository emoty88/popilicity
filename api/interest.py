from popilicity.models import Interest
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class InterestSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:interest-detail")
    class Meta:
        model = Interest
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
class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
