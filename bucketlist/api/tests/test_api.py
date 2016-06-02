from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import CustomUser, BucketList, BucketListItem
from django.test import Client


class UserAPITestCase(APITestCase):
    """Tests for user api authorizaion."""

    def setUp(self):
        self.client = Client()

    def test_user_creation(self):
        """Test user can create account"""
        resp = self.client.post('/api/register/', {'username': 'samantha',
                                        'email': 'sam@gmail.com',
                                        'password': 'password'})

        self.assertEqual(resp.status_code, 201)

    def test_unauthorized_access(self):
        """Test that user cannot access bucketlist if not authorized."""
        resp = self.client.get('bucket_detail')
        self.assertEqual(resp.status_code, 404)


class BucketlistAPITestCase(APITestCase):
    """Test buckelist methods"""

    def setUp(self):
        resp = self.client.post('/api/register/', {'username': 'samantha',
                                        'email': 'sam@gmail.com',
                                        'password': 'password'})

        token_url = reverse('logins')
        data = {
            'username': 'samantha', 'password': 'password'}
        response = self.client.post(token_url, data)
        token = 'JWT ' + response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_bucketlist_creation(self):
        """Tests that user can create bucketlists"""
        # Issue a POST request.
        resp = self.client.post('/api/bucketlist/create/', {'name': 'bucketlist'}, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_bucketlist_details(self):
        """Test that it return bucketlists"""
        # Issue a GET request.
        response = self.client.get('/api/bucketlist/')
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_edit(self):
        """Test that a user can edit a bucketlist"""

        create_resp = self.client.post('/api/bucketlist/create/', {'name': 'surfing',},)
        edit_resp = self.client.put('/api/bucketlist/3/edit/', { 'name': 'paragliding',},)
        self.assertEqual(edit_resp.status_code, 200)

    def test_bucketlist_delete(self):
        """Test that a user can delete a bucketlist."""
        create_resp = self.client.post('/api/bucketlist/create/', {'name': 'surfing',},)
        bid = BucketList.objects.all()[0].id
        delete_resp = self.client.delete('/api/bucketlist/' + str(bid) +'/delete/')
        self.assertEqual(delete_resp.status_code, 204)


class BucketlistItemAPITestCase(APITestCase):
    """Test buckelistitem methods"""

    fixtures = ['initial_data.json']

    def setUp(self):
        resp = self.client.post('/api/register/', {'username': 'samantha',
                                        'email': 'sam@gmail.com',
                                        'password': 'password'})
        token_url = reverse('logins')
        data = {
            'username': 'samantha', 'password': 'password'}
        response = self.client.post(token_url, data)
        token = 'JWT ' + response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_bucketlist_item_creation(self):
        """Test that a user can create a bucketlist item."""
        resp = self.client.post('/api/bucketlist/1/items/', {'name': 'hiking'})
        self.assertEqual(resp.status_code, 201)

    def test_bucketlistitem_edit(self):
        """Test that a bucketlistitem can be updated."""

        edited_item = {'name': 'sunrise', 'bucketlist': 1}

        resp = self.client.put('/api/bucketlist/1/items/1', edited_item)
        self.assertEqual(resp.status_code, 200)

    def test_deleting_bucketlist_item(self):
        """Test that a bucketlistitem can be deleted"""
        self.client.post('/api/bucketlist/1/items/1', {'name': 'hiking', 'done': 'False'})
        delete_resp = self.client.delete('/api/bucketlist/1/items/1')
        self.assertEqual(delete_resp.status_code, 204)