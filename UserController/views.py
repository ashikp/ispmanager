from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser, Role
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def getAllCustomers(request):
    customer_role = Role.objects.get(name="Customer")
    # Get all CustomUser instances
    users = CustomUser.objects.filter(role=customer_role)

    
    # Serialize the user data
    serializer = CustomUserSerializer(users, many=True)
    
    # Return the serialized data
    return Response(serializer.data, status=200)