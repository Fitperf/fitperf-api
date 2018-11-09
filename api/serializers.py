from rest_framework import serializers
from .models import Equipment, Movement

class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'founder')
        model = Equipment

class MovementSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'equipment', 'founder', 'settings')
        model = Movement