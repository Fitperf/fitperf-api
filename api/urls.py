from django.urls import path

from .views import EquipmentList, EquipmentDetail, MovementList, MovementDetail

urlpatterns = [
    path('equipment/', EquipmentList.as_view()),
    path('equipment/<int:pk>/', EquipmentDetail.as_view()),
    path('movement/', MovementList.as_view()),
    path('movement/<int:pk>/', MovementDetail.as_view()),
]