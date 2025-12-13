from rest_framework.response import Response
from rest_framework.decorators import api_view
from cities.models import City
from .serializers import ItemSerializer

@api_view(['GET'])
def getData(request):
    cities = City.objects.all()
    serializer = ItemSerializer(cities, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addCity(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()