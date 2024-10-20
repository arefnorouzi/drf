import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Post


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def test_user2():
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def test_post(test_user):
    return Post.objects.create(
        title='Test Post',
        description='Test Content',
        author=test_user
    )


@pytest.fixture
def test_posts(test_user, test_user2):
    posts = [
        Post.objects.create(
            title=f'Test Post {i}',
            description=f'Test Content {i}',
            author=test_user if i % 2 == 0 else test_user2
        ) for i in range(5)
    ]
    return posts


@pytest.mark.django_db
class TestPostAPI:
    def test_create_post_authenticated(self, authenticated_client):
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'description': 'New Content'
        }

        response = authenticated_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Post'
        assert response.data['description'] == 'New Content'
        assert 'author_name' in response.data
        assert 'created_at' in response.data
        assert Post.objects.count() == 1

    def test_create_post_unauthenticated(self, api_client):
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'description': 'New Content'
        }

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Post.objects.count() == 0

    def test_create_post_invalid_data(self, authenticated_client):
        url = reverse('post-list')
        data = {
            'title': '',  # Empty title should be invalid
            'description': 'New Content'
        }

        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Post.objects.count() == 0

    def test_get_post_list(self, api_client, test_posts):
        url = reverse('post-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5
        assert all(
            isinstance(post['title'], str) and
            isinstance(post['description'], str)
            for post in response.data
        )

    def test_get_post_detail(self, api_client, test_post):
        url = reverse('post-detail', kwargs={'pk': test_post.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == test_post.title
        assert response.data['description'] == test_post.description
        assert 'author_name' in response.data
        assert 'created_at' in response.data

    def test_get_post_detail_not_found(self, api_client):
        url = reverse('post-detail', kwargs={'pk': 999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_post_owner(self, authenticated_client, test_post):
        url = reverse('post-detail', kwargs={'pk': test_post.pk})
        data = {
            'title': 'Updated Title',
            'description': 'Updated Content'
        }

        response = authenticated_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        assert response.data['description'] == 'Updated Content'

        test_post.refresh_from_db()
        assert test_post.title == 'Updated Title'
        assert test_post.description == 'Updated Content'

    def test_partial_update_post_owner(self, authenticated_client, test_post):
        url = reverse('post-detail', kwargs={'pk': test_post.pk})
        data = {
            'title': 'Updated Title Only'
        }

        response = authenticated_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title Only'
        assert response.data['description'] == test_post.description

    def test_update_post_non_owner(self, api_client, test_post, test_user2):
        api_client.force_authenticate(user=test_user2)
        url = reverse('post-detail', kwargs={'pk': test_post.pk})
        data = {
            'title': 'Updated Title',
            'description': 'Updated Content'
        }

        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        test_post.refresh_from_db()
        assert test_post.title == 'Test Post'

    def test_delete_post_owner(self, authenticated_client, test_post):
        url = reverse('post-detail', kwargs={'pk': test_post.pk})
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(pk=test_post.pk).exists()

    def test_delete_post_non_owner(self, api_client, test_post, test_user2):
        api_client.force_authenticate(user=test_user2)
        url = reverse('post-detail', kwargs={'pk': test_post.pk})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Post.objects.filter(pk=test_post.pk).exists()
