from popilicity.models import ReportedPost
from rest_framework import routers, serializers, viewsets
import autoActions
from rest_framework.validators import UniqueTogetherValidator
#from api.user import UserSerializer
#from api.post import PostSerializer

# Serializers define the API representation.
class ReportedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedPost
        fields = ('id', 'post_is_reported', 'reason')
        extra_kwargs = {'user_is_reporting': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        # post_is_reported = self.initial_data['post_is_reported']

        (rp, is_not_found) = ReportedPost.objects.get_or_create(user_is_reporting_id=user.id, **validated_data)
        if is_not_found:
            rp.save()

        return rp


# ViewSets define the view behavior.
class ReportedPostViewSet(viewsets.ModelViewSet):
    queryset = ReportedPost.objects.all()
    serializer_class = ReportedPostSerializer
