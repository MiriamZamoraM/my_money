from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.

class PostAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None, *args, **kwargs):
        post = Profile.objects.all()
        serializer = ProfileSerializer(post, many=True)
        return Response(serializer.data)
