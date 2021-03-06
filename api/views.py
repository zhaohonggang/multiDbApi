from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework_expiring_authtoken.authentication import ExpiringTokenAuthentication
#from .serializers import ArticleSerializer, CommentSerializer, TagSerializer
from rest_framework.decorators import api_view, authentication_classes
#from blog.models import Article, Comment, Tag
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework_expiring_authtoken.models import ExpiringToken
#from .paginator import get_page_list
from django.core.paginator import Paginator
import datetime



# Create your views here.
class UserLoginAPIView(APIView):
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = ExpiringToken.objects.get_or_create(user=user)
            response = Response('Setting a cookie')
            #response.set_cookie('cookie', 'MY COOKIE VALUE')
            response.set_cookie('Token', token.key)
            if not created:
                token.created = datetime.datetime.utcnow()
                token.save()
            return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((ExpiringTokenAuthentication,))
def request_user(request):
    print(request.auth)
    if request.auth:
        user_info = request.user
        token = ExpiringToken.objects.first()
        token.created = datetime.datetime.utcnow()
        token.save()
        return Response({'user': str(user_info)}, status=status.HTTP_200_OK)
    else:
        return Response({'user': 'not_login'}, status=status.HTTP_401_UNAUTHORIZED)