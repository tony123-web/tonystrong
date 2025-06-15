#from  django.http import JsonResponse
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from my_app.models import Room
from .serielizer import Roomserializer

@api_view(['GET'])
def geteRoutes(request):
    routes =[
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serialized = Roomserializer(rooms, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serialized = Roomserializer(room, many=False)
    return Response(serialized.data)