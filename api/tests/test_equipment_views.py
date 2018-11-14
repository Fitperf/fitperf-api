from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Equipment
from .helper_dbtestdata import TestDatabase

class EquipmentTest(APITestCase):
    """
    This class will test all the interactions we can have with
    Equipment views. What will be tested:
        -> Not Connected:
            FAIL:
                -> Get all equipments
                -> Get one specific equipment
        -> With admin account:
            SUCCESS:
                -> Get all equipments
                -> Get one specific equipment
                -> Create a new equipment
                -> Delete an equipment
                -> Modify an equipment
            FAIL:
                -> Create a new equipment where the name already exists
        -> With non admin account:
            SUCCESS:
                -> Get all the equipments
                -> Get one specific equipment
            FAIL:
                -> Create a new equipment
                -> Delete a equipment
                -> Modify a equipment
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a database for test with TestDatabase helper
        """
        TestDatabase.create()

    def test_not_connected_get_all_equipements(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        """
        url = reverse('equipments_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_not_connected_get_one_equipment(self):
        """
        Test if, we are not authenticated, the API returns a 403 status on this request
        """
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_equipements(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - all the equipments
        """
        self.client.login(username='admin_user', password='admin_password')
        url = reverse('equipments_list')
        equipments = Equipment.objects.count()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), equipments)
    
    def test_admin_get_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API returns:
            - a 200 status on this request
            - get the adequate equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        kb = Equipment.objects.get(name="kettlebell")

        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        equipment_response = {
            'id': kb.pk,
            'name': kb.name,
            'founder': kb.founder.pk
        }
        self.assertEqual(response.data, equipment_response)

    def test_admin_create_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API creates correctly
        the equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        initial_equipments = Equipment.objects.count()
        url = reverse('equipments_list')
        data = {
            'name': 'box',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), initial_equipments + 1)

    def test_admin_create_one_equipment_which_already_exists(self):
        """
        Test if, when we are logged with an admin account, the API does not create
        the equipment because the name is already used in the database
        """
        self.client.login(username='admin_user', password='admin_password')
        founder = User.objects.get(username='admin_user')
        initial_equipments = Equipment.objects.count()
        url = reverse('equipments_list')
        data = {
            'name': 'kettlebell',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Equipment.objects.count(), initial_equipments)


    def test_admin_update_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API updates correctly
        the equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        data = {
            "id": kb.pk,
            "name": "big kettlebell",
            "founder": kb.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": kb.pk, "name": "big kettlebell", "founder": kb.founder.pk})

    def test_admin_delete_one_equipment(self):
        """
        Test if, when we are logged with an admin account, the API deletes correctly the equipment
        """
        self.client.login(username='admin_user', password='admin_password')
        initial_equipments = Equipment.objects.count()
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.count(), initial_equipments - 1)

    def test_non_admin_get_all_equipements(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - all the equipments
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        url = reverse('equipments_list')
        equipments = Equipment.objects.count()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), equipments)
    
    def test_non_admin_get_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API returns:
            - a 200 status on this request
            - get the adequate equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        kb = Equipment.objects.get(name="kettlebell")

        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        equipment_response = {
            'id': kb.pk,
            'name': kb.name,
            'founder': kb.founder.pk
        }
        self.assertEqual(response.data, equipment_response)

    def test_non_admin_create_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API does not create
        the equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        founder = User.objects.get(username='ordinary_user')
        initial_equipments = Equipment.objects.count()
        url = reverse('equipments_list')
        data = {
            'name': 'box',
            'founder': founder.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Equipment.objects.count(), initial_equipments)

    def test_non_admin_update_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API does not update
        the equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        data = {
            "id": kb.pk,
            "name": "big kettlebell",
            "founder": kb.founder.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_delete_one_equipment(self):
        """
        Test if, when we are logged with a non admin account, the API does not delete the
        equipment
        """
        self.client.login(username='ordinary_user', password='ordinary_password')
        initial_equipments = Equipment.objects.count()
        kb = Equipment.objects.get(name="kettlebell")
        url = reverse('equipment_detail', kwargs={'pk': kb.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Equipment.objects.count(), initial_equipments)