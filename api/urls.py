from django.urls import path

from .views import EquipmentList, EquipmentDetail, MovementList, MovementDetail, MovementSettingsList, MovementSettingsDetail

urlpatterns = [
    path('equipments/', EquipmentList.as_view(), name='equipments_list'),
    path('equipments/<int:pk>/', EquipmentDetail.as_view(), name='equipment_detail'),
    path('movements/', MovementList.as_view(), name='movements_list'),
    path('movements/<int:pk>/', MovementDetail.as_view(), name="movement_detail"),
    path('movement-settings/', MovementSettingsList.as_view(), name='movement_settings_list'),
    path('movement-settings/<int:pk>/', MovementSettingsDetail.as_view(), name='movement_setting_detail'),
]