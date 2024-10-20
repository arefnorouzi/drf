from django.test import TestCase
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()


def posts():
    request = factory.get('/posts')
