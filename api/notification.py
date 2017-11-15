from popilicity.models import Notification
from rest_framework import routers, serializers, viewsets, filters
#from api.Base64ImageField import Base64ImageField
from drf_extra_fields.fields import Base64ImageField
from api.user import UserSerializer
from api.post import PostSerializer
#import django_filters.rest_framework
from rest_framework import generics
from api.customPagination import CustomPageNumberPagination
import autoActions
import django_filters

# Serializers define the API representation.
class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    owner       = UserSerializer()
    target_usr  = UserSerializer()
    target_post = PostSerializer()

    class Meta:
        model = Notification
        fields = (
            'id',
            'owner',
            'target_usr',
            'target_post',
            'is_seen',
            'action',
            'create_date',
            'update_date',
        )


# ViewSets define the view behavior.
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        print(self.request.GET)
        if('count' not in self.request.GET):
            Notification.objects.all().filter(target_usr_id=self.request.user.id).filter(is_seen=0).update(is_seen=1)
        notifications = Notification.objects.all().filter(target_usr_id=self.request.user.id).order_by('-create_date')
        return notifications
