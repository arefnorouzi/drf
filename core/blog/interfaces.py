from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .models import Post


class IPostRepository(ABC):
    @abstractmethod
    def get_all(self) -> List['Post']:
        pass

    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional['Post']:
        pass

    @abstractmethod
    def create(self, post_data: dict) -> 'Post':
        pass

    @abstractmethod
    def update(self, post_id: int, post_data: dict) -> Optional['Post']:
        pass

    @abstractmethod
    def delete(self, post_id: int) -> bool:
        pass


class IPostService(ABC):
    @abstractmethod
    def get_all_posts(self) -> List['Post']:
        pass

    @abstractmethod
    def get_post(self, post_id: int) -> Optional['Post']:
        pass

    @abstractmethod
    def create_post(self, post_data: dict, author: 'User') -> 'Post':
        pass

    @abstractmethod
    def update_post(self, post_id: int, post_data: dict, user: 'User') -> Optional['Post']:
        pass

    @abstractmethod
    def delete_post(self, post_id: int, user: 'User') -> bool:
        pass
