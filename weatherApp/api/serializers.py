from rest_framework import serializers
from cities.models import City

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'