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
from django.conf import settings
from django.http import HttpResponse
from .tasks import hello_mail
from .throttles import AnonRateThrottles, SustainedRateThrottle
class TodoView(ListAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()  

class RegisterUserView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    
class LoginUserView(APIView):
    serializer_class = LoginUserSerializer
    authentication_classes = [TokenAuthentication]
    throttle_classes = [AnonRateThrottles, SustainedRateThrottle]
    
    def post(self, request):
        user = authenticate(email = request.data['email'], password = request.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key , "Success": "Successfully logged in"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)   

class ListTasksView(APIView):
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
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        user = request.user
        if type(user.id) != (int):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"success": "Task Created Successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class UpdateTaskView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateSerializer
    
    def patch(self, request, pk):
        import pdb;pdb.set_trace()
        
        # import pdb;pdb.set_trace()
        to_do = get_object_or_404(Todo, id=pk)
        serializer = UpdateSerializer(to_do, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['status'] == 'Completed':
            completed_date = date.today()
            serializer.validated_data['complete_date'] = completed_date
        
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
def sendMail(request):
    email = 'shivanshkaurav05@gmail.com'
    hello_mail.delay(email)
    
    return HttpResponse("Email sent!")