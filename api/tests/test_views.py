import json
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

    def test_not_connected_get_all_movement_settings(self):
        """
        Test if, we are not authenticated,  the API returns a 403 status on this request
        """
        url = reverse('movement_settings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_not_connected_get_one_movement_settings(self):
        """
        Test if, we are not authenticated,  the API returns a 403 status on this request
        """
        url = reverse('movement_setting_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - all the movement settings
        """
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('movement_settings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_admin_get_one_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - get the adequate movement
        """
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('movement_setting_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'repetitions', 'founder': 1})

    def test_admin_create_one_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API creates correctly
        the movement settings
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        initial_movement_settings = MovementSettings.objects.count()
        url = reverse('movement_settings_list')
        data = {
            'name': 'lestes',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MovementSettings.objects.count(), initial_movement_settings + 1)

    def test_admin_update_one_movement_settings_in_list(self):
        """
        Test if, when we are logged with an admin account, the API does not updates the movement settings
        because the name is in the choice list
        """
        self.client.login(username='admin_user', password='admin_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        data = {
            "id": rep.pk,
            "name": MovementSettings.LEST,
            "founder": rep.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": rep.pk, "name": "lestes", "founder": rep.founder.pk})

    def test_admin_update_one_movement_settings_not_in_list(self):
        """
        Test if, when we are logged with an admin account, the API does not update the movement settings
        because it is not in the choice list
        """
        self.client.login(username='admin_user', password='admin_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        data = {
            "id": rep.pk,
            "name": "new_repetitions",
            "founder": rep.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_one_movement_settings(self):
        """
        Test if, when we are logged with an admin account, the API deletes correctly the movement settings
        """
        self.client.login(username='admin_user', password='admin_password')
        initial_movement_settings = MovementSettings.objects.count()
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        data = {
            "id": rep.pk,
            "name": rep.name,
            "founder": rep.founder.pk
        }
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MovementSettings.objects.count(), initial_movement_settings - 1)

    def test_non_admin_get_all_movement_settings(self):
        """
        Test if, when we are logged with a non-admin account, the API returns:
            - a 200 status on this request
            - all the movement settings
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        url = reverse('movement_settings_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_non_admin_get_one_movement_settings(self):
        """
        Test if, when we are logged with a non-admin account, the API returns:
            - a 200 status on this request
            - get the adequate movement
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        url = reverse('movement_setting_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'name': 'repetitions', 'founder': 1})

    def test_non_admin_create_one_movement_settings(self):
        """
        Test if, when we are logged with a non admin account, the API forbids the creation of
        a movement settings
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        founder = User.objects.get(username='ordinary_user')
        initial_movement_settings = MovementSettings.objects.count()
        url = reverse('movement_settings_list')
        data = {
            'name': 'lestes',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MovementSettings.objects.count(), initial_movement_settings)

    def test_non_admin_update_one_movement_settings(self):
        """
        Test if, when we are logged with a non admin account, the API does not allowed the 
        update.
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        data = {
            "id": rep.pk,
            "name": MovementSettings.LEST,
            "founder": rep.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_delete_one_movement_settings(self):
        """
        Test if, when we are logged with a non admin account, the API does not allowed the 
        deleting.
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        initial_movement_settings = MovementSettings.objects.count()
        rep = MovementSettings.objects.get(name=MovementSettings.REPETITIONS)
        data = {
            "id": rep.pk,
            "name": rep.name,
            "founder": rep.founder.pk
        }
        url = reverse('movement_setting_detail', kwargs={'pk': rep.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
