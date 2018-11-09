from django.urls import path

from .views import UserList, UserDetail, EquipmentList, EquipmentDetail, MovementList, MovementDetail, MovementSettingsList, MovementSettingsDetail

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('equipments/', EquipmentList.as_view()),
    path('equipments/<int:pk>/', EquipmentDetail.as_view()),
    path('movements/', MovementList.as_view()),
    path('movements/<int:pk>/', MovementDetail.as_view()),
    path('movement-settings/', MovementSettingsList.as_view()),
    path('movement-settings/<int:pk>/', MovementSettingsDetail.as_view()),
]