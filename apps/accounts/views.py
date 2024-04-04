from django.shortcuts import get_object_or_404
from .models import Account
from .serializers import AccSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
    
class PostAccount(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        data = request.data
        data['user_id']=request.user.id
        serializer = AccSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get (self, request):
        accounts_list = Account.objects.filter(user_id=request.user, status_delete=False)
        serializer = AccSerializer(accounts_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class IDAccountAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, account_id):
        account_obj = Account.objects.filter(user_id=request.user, pk=account_id, status_delete=False)
        serializer = AccSerializer(account_obj, many=True)
        return Response(serializer.data)
    
    def put(self, request, account_id):
        
        account_obj = get_object_or_404(Account, pk=account_id, status_delete=False)
        serializer = AccSerializer(instance=account_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, account_id):
        account_obj = get_object_or_404(Account, pk=account_id, status_delete=False)
        account_obj.status_delete = True
        account_obj.save()
        return Response({'message':'Eliminado'}, status=status.HTTP_204_NO_CONTENT)