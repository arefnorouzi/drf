from django.shortcuts import get_object_or_404
from typing import List, Optional
from .interfaces import IPostRepository
from .models import Post
from django.core.exceptions import PermissionDenied


class PostRepository(IPostRepository):
    def get_all(self) -> List[Post]:
        return Post.objects.select_related('author').all()

    def get_by_id(self, post_id: int) -> Optional[Post]:
        return get_object_or_404(Post.objects.select_related('author'), id=post_id)

    def create(self, post_data: dict) -> Post:
        return Post.objects.create(**post_data)

    def update(self, post_id: int, post_data: dict) -> Optional[Post]:
        post = self.get_by_id(post_id)
        for key, value in post_data.items():
            setattr(post, key, value)
        post.save()
        return post

    def delete(self, post_id: int) -> bool:
        post = self.get_by_id(post_id)
        post.delete()
        return True