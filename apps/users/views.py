from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer

class RegistryView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class ListApiView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request):
        users_list = User.objects.all().filter(status_delete=False)
        serializer = UserSerializer(users_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)