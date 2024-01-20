from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import QASerializer
from .models import QA



class QAView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *arg, **kwargs):
        QAs = QA.objects.all()
        serialized_data = QASerializer(QAs, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
