from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import CustomUserSerializer, SignupSerializer
User = get_user_model()

@api_view(['GET'])
def index(_self):
    return Response({'hello': 'world'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    
    # Validate the incoming data
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate a token for the newly created user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role.name  # Role name
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    # Check if username and password are provided in the request data
    if 'username' not in request.data or 'password' not in request.data:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Get the user using the username provided in the request
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the password is correct
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_404_NOT_FOUND)

    # Get or create an authentication token for the user
    token, created = Token.objects.get_or_create(user=user)

    # Serialize the user data
    serializer = CustomUserSerializer(user)

    # Return the token and user data in the response
    return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)