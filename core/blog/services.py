from .models import Post, User
from .interfaces import IPostRepository, IPostService
from django.core.exceptions import PermissionDenied
from typing import List, Optional


class PostService(IPostService):
    def __init__(self, post_repository: IPostRepository):
        self._post_repository = post_repository

    def get_all_posts(self) -> List[Post]:
        return self._post_repository.get_all()

    def get_post(self, post_id: int) -> Optional[Post]:
        return self._post_repository.get_by_id(post_id)

    def create_post(self, post_data: dict, author: 'User') -> Post:
        post_data['author'] = author
        return self._post_repository.create(post_data)

    def update_post(self, post_id: int, post_data: dict, user: 'User') -> Optional[Post]:
        post = self.get_post(post_id)
        if post.author != user:
            raise PermissionDenied("You don't have permission to update this post")
        return self._post_repository.update(post_id, post_data)

    def delete_post(self, post_id: int, user: 'User') -> bool:
        post = self.get_post(post_id)
        if post.author != user:
            raise PermissionDenied("You don't have permission to delete this post")
        return self._post_repository.delete(post_id)
