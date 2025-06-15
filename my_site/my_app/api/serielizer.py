from rest_framework.serializers import ModelSerializer
from my_app.models import Room

class Roomserializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'