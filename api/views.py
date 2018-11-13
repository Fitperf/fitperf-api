from rest_framework import generics, permissions

from django.contrib.auth.models import User
from .models import Equipment, Movement, MovementSettings, Exercise
from .serializers import EquipmentSerializer, MovementSerializer, MovementSettingsSerializer, ExerciseSerializer
from .permissions import IsAdminOrReadOnly, IsFounderOrReadOnly, IsAdminOrFounderOrReadOnly

class EquipmentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly,)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class EquipmentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly,)
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class MovementList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly,)
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

class MovementDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly,)
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

class MovementSettingsList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly,)
    queryset = MovementSettings.objects.all()
    serializer_class = MovementSettingsSerializer

class MovementSettingsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly,)
    queryset = MovementSettings.objects.all()
    serializer_class = MovementSettingsSerializer

class ExerciseList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrFounderOrReadOnly)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrFounderOrReadOnly)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer