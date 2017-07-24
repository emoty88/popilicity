from popilicity.models import Rate
from rest_framework import routers, serializers, viewsets
import autoActions
#from api.user import UserSerializer
#from api.post import PostSerializer

# Serializers define the API representation.
class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('id', 'post_id', 'user_id', 'rate')

    def create(self, validated_data):
        post_id = self.initial_data['post_id']
        user = self.context['request'].user
        (rate, is_not_found) = Rate.objects.get_or_create(user_id=user.id, post_id=int(post_id))

        if is_not_found:
            oldRate = False
        else:
            oldRate = rate.rate

        rate.rate = validated_data['rate']
        rate.save()
        autoActions.postRate(post_id, rate.rate, oldRate, user)
        return rate


# ViewSets define the view behavior.
class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
