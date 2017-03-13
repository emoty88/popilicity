from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
#from django.shortcuts import get_object_or_404
#from rest_framework.response import Response

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")
    class Meta:
        model = User
        fields = ( 'password', 'username', 'email', 'first_name', 'last_name',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        #return Snippet.objects.create(**validated_data)
        # call set_password on user object. Without this
        # the password will be stored in plain text.
        # print validated_data
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'
