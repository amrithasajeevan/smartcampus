from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.
class RegisterAPIView(APIView):
    def get(self, request):
        # Retrieve all CustomUser objects
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({'status':1,'data':serializer.data})

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send email to the user with their information
            subject = 'Account Created Successfully'
            message = f'Hi {user.first_name},\n\nYour account has been created successfully.\n\nName: {user.first_name} {user.last_name}\nAdmission Number: {user.admission_number}\nPassword: {request.data["password"]}\n\nThank you!'
            from_email = 'amrithababy142@email.com'  # Replace with your email
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return Response({'status':1,'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status':0,'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = Loginserializer(data=request.data)
        if serializer.is_valid():
            admission_number = serializer.validated_data['admission_number']
            password = serializer.validated_data['password']
            user = CustomUser.objects.filter(admission_number=admission_number).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 1,
                    'data':{
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user_id': user.id,
                    'username': user.username,
                    'admission_number': user.admission_number,
                    'email': user.email
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'status': 0, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 0, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


class AddAttendance(APIView):
    def get(self, request, admission_number):
        user = get_object_or_404(CustomUser, admission_number=admission_number)
        attendance = Attendance.objects.filter(user=user).order_by('-timestamp').first()
        if attendance:
            attendance_data = {
                "user_id": attendance.user.id,
                "username": attendance.user.username,
                "admission_number": attendance.user.admission_number,
                "timestamp": attendance.timestamp
            }
            return Response(attendance_data)
        else:
            return Response({"message": "Attendance not found for this user"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, admission_number):
        try:
            user = CustomUser.objects.get(admission_number=admission_number)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        attendance = Attendance(user=user)
        attendance.save()

        attendance_data = {
            "user_id": user.id,
            "username": user.username,
            "admission_number": user.admission_number,
            "timestamp": attendance.timestamp
        }

        return Response({
            'status': 1,
            "message": "Attendance added successfully",
            'data': attendance_data
        })


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response({'status':1,'data':serializer.data})

    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':1,'data':serializer.data})
        return Response({'status': 0, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


from rest_framework_simplejwt.authentication import JWTAuthentication

class ViewAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        attendance_records = Attendance.objects.filter(user=user)
        attendance_data = [
            {"timestamp": record.timestamp} for record in attendance_records
        ]
        return Response(attendance_data)