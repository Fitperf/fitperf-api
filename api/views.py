from rest_framework import generics, permissions

from django.db.models import Q
from django.contrib.auth.models import User
from .models import Equipment, Movement, MovementSettings, Exercise, MovementsPerExercise, Training
from .serializers import EquipmentSerializer, MovementSerializer, MovementSettingsSerializer, ExerciseSerializer, TrainingSerializer
from .permissions import IsAdminOrReadOnly, IsExerciseDefaultOrIsAdminOrFounder, IsFounderOrReadOnly, IsAdminOrFounderOrReadOnly, IsAdminOrFounder

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
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Exercise.objects.all()
        return Exercise.objects.filter(Q(is_default=True) | Q(founder=self.request.user))

class ExerciseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsExerciseDefaultOrIsAdminOrFounder)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class TrainingList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrFounder)
    serializer_class = TrainingSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Training.objects.all()
        return Training.objects.filter(founder=self.request.user)

class TrainingDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdminOrFounder)
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer