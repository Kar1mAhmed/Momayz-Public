
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AreaSerializer, GovernSerializer
from .models import Area, Govern




class GovernView(APIView):
    def get(self, request, *args, **kwargs):
        governs = Govern.objects.all()
        serialized_data = GovernSerializer(governs, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    



class AreaView(APIView):
    def get(self, request, *args, **kwargs):
        requested_govern = request.GET.get('govern_id')
        if requested_govern is None:
            requested_govern = 1
        cites = Area.objects.filter(govern=requested_govern, city=True)
        serialized_data = AreaSerializer(cites, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    
