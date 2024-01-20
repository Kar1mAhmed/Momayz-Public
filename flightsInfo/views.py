from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import Package
from .serializers import PackageSerializer, AppointmentsSerializer

from flights.models import Program


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_packages(request):
    packages = Package.objects.filter(city=request.user.city)
    serialized_packages = PackageSerializer(packages, many=True)
    return Response(serialized_packages.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def return_appointments(request):
    user = request.user
    appointments = Program.objects.get(move_to=user.city).move_at.all()
    serializer = AppointmentsSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def go_appointments(request):
    user = request.user
    appointments = Program.objects.get(move_from=user.city).move_at.all()
    serializer = AppointmentsSerializer(appointments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
