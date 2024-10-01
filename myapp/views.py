from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from .models import Todo
from .serializers import *
from rest_framework.views import APIView
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from .throttles import AnonRateThrottles, SustainedRateThrottle

class TodoView(ListAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()  

class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    
class LoginUserView(APIView):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    throttle_classes = [AnonRateThrottles, SustainedRateThrottle]
    
    def post(self, request):
        user = authenticate(email = request.data['email'], password = request.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key , "Success": "Successfully logged in"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)   

class ListTasksView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TodoSerializer
    
    def get(self, request):
        user = request.user
        if type(user.id) != (int):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        todo = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todo, many=True)
        data = serializer.data
        return Response({"data": data}, status=status.HTTP_200_OK)   

class CreateTaskView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TodoSerializer
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            to_do_item = serializer.save(user=user)
            return Response({"success": "Task Created Successfully!", "id": to_do_item.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class UpdateTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSerializer
    
    def patch(self, request, pk):
        to_do = get_object_or_404(Todo, id=pk)
        serializer = UpdateSerializer(to_do, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['status'] == 'Completed':
            completed_date = date.today()
            serializer.validated_data['complete_date'] = completed_date
        
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_200_OK)