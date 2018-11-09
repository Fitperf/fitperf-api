from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Equipment, Movement, MovementSettings
from .helper_dbtestdata import TestDatabase

class MovementSettingsTest(APITestCase):
    """
    This class will test all the interactions we can have with
    MovementSettings class. What will be tested:
        -> Not Connected:
            FAIL:
                -> Get all movement's settings
                -> Get one specific movement setting
        -> With admin account:
            SUCCESS:
                -> Get all movement's settings
                -> Get one specific movement setting
                -> Create a new movementsetting in list choice
                -> Delete a movement setting
                -> Modify a movement setting
            FAIL:
                -> Create a new movementsetting not in the list
        -> With non admin account:
            SUCCESS:
                -> Get all the movement's settings
                -> Get one specific movement setting
            FAIL:
                -> Create a new movementsetting in list choice
                -> Delete a movement setting
                -> Modify a movement setting
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def test_not_connected_get_all_movementsettings(self):
        url = reverse('movement_settings_list')
        response = self.client.get(url, format='json')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)