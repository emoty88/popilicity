from popilicity.models import Notification
# from notification import NotificationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NotificationCount(APIView):
    def get(self, request, format=None):
        notifications = Notification.objects.all().filter(target_usr_id=request.user.id, is_seen=0).count()
        return Response(int(notifications))
