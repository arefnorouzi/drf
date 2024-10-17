from rest_framework import status, viewsets
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from .serializers import PostInputSerializer, PostOutputSerializer
from .services import PostService
from .repositories import PostRepository
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._post_service = PostService(PostRepository())

    def list(self, request):
        posts = self._post_service.get_all_posts()
        serializer = PostOutputSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post = self._post_service.get_post(pk)
        serializer = PostOutputSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostInputSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = self._post_service.create_post(
                    serializer.validated_data,
                    request.user
                )
                return Response(
                    PostOutputSerializer(post).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = PostInputSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                post = self._post_service.update_post(
                    pk,
                    serializer.validated_data,
                    request.user
                )
                return Response(PostOutputSerializer(post).data)
            except PermissionDenied as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_403_FORBIDDEN
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            self._post_service.delete_post(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

