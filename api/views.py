from rest_framework import generics

from django.contrib.auth.models import User
from .models import Equipment, Movement, MovementSettings
from .serializers import EquipmentSerializer, MovementSerializer, MovementSettingsSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly, IsFounderOrReadOnly

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EquipmentList(generics.ListCreateAPIView):
    permissions_classes = (IsFounderOrReadOnly,)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class EquipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permissions_classes = (IsFounderOrReadOnly,)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class MovementList(generics.ListCreateAPIView):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

class MovementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

class MovementSettingsList(generics.ListCreateAPIView):
    queryset = MovementSettings.objects.all()
    serializer_class = MovementSettingsSerializer

class MovementSettingsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovementSettings.objects.all()
    serializer_class = MovementSettingsSerializer