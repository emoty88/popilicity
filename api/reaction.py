from popilicity.models import Reaction
from rest_framework import routers, serializers, viewsets
import autoActions
#from api.user import UserSerializer
#from api.post import PostSerializer

# Serializers define the API representation.
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'post_id', 'user_id', 'type')

    def create(self, validated_data):
        post_id = self.initial_data['post_id']
        user = self.context['request'].user
        (reaction, is_not_found) = Reaction.objects.get_or_create(user_id=user.id, post_id=int(post_id))

        if is_not_found:
            oldReaction = False
        else:
            oldReaction = reaction.type

        reaction.type = validated_data['type']
        reaction.save()
        autoActions.postReaction(post_id, reaction.type, oldReaction, user)
        return reaction


# ViewSets define the view behavior.
class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
