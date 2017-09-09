from popilicity.models import Block
from rest_framework import routers, serializers, viewsets
import autoActions
from rest_framework.validators import UniqueTogetherValidator
#from api.user import UserSerializer
#from api.post import PostSerializer

# Serializers define the API representation.
class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ('id', 'user_is_blocking', 'user_is_blocked')
        extra_kwargs = {'user_is_blocking': {'read_only': True}}


    def validate(self, data):
        user_id = int(self.context['request'].user.id)
        if int(data['user_is_blocked'].id) is user_id:
            raise serializers.ValidationError("You cannot block yourself.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user_is_blocked = self.initial_data['user_is_blocked']

        (block, is_not_found) = Block.objects.get_or_create(user_is_blocking_id=user.id, user_is_blocked_id=int(user_is_blocked))
        print(is_not_found)
        print(type(int(user.id)))
        print(type(int(user_is_blocked)))
        print((int(user.id) is not int(user_is_blocked)))
        if is_not_found:
            print ('block saved.')
            block.save()

        return block


# ViewSets define the view behavior.
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
