# freshlyapp/tests/test_posts.py

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Post

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username='testuser', password='testpass')
    return client

@pytest.fixture
def post(user):
    return Post.objects.create(title='Test Post', content='Test Content', author=user)

def test_create_post(client):
    response = client.post('/freshlyapp/posts/', {'title': 'New Post', 'content': 'New Content'})
    assert response.status_code == 201
    assert Post.objects.count() == 1

def test_update_post(client, post):
    response = client.put(f'/freshlyapp/posts/{post.id}/', {'title': 'Updated Post', 'content': 'Updated Content'})
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.title == 'Updated Post'
    assert post.content == 'Updated Content'

def test_delete_post(client, post):
    response = client.delete(f'/freshlyapp/posts/{post.id}/')
    assert response.status_code == 204
    assert Post.objects.count() == 0
