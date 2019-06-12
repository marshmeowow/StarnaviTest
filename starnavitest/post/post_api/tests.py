from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from post.models import Post
from rest_framework.reverse import reverse

User = get_user_model()


class PostAPITestCase(APITestCase):

    def setUp(self):
        user = User(username='TestUser', email='test@test.com')
        user.set_password("123123123")
        user.save()
        post = Post.objects.create(user=user, content="TTTTEEEESSSTTT!!!!")

    def test_get_list(self):
        data = {}
        url = reverse('post-list-create')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {'content': 'WAAAATEEEERR!!!!'}
        url = reverse('post-list-create')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_like_auth(self):
        post = Post.objects.first()
        data = {}
        url = post.get_api_url()
        response = self.client.post(url + 'like/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url + 'unlike/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login(self):
        data = {'username': 'TestUser', 'password': '123123123'}
        url = 'http://127.0.0.1:8000/api/auth/login/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            post = Post.objects.first()
            data = {}
            url = post.get_api_url()
            response = self.client.post(url + 'like/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.post(url + 'unlike/', data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response = self.client.delete(post.get_api_url())
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_registration(self):
        data = {
                "username": "TestUser2",
                "email": "testmail@mail.com",
                "password1": "A23123123",
                "password2": "A23123123"
        }
        url = 'http://127.0.0.1:8000/api/auth/registration/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
