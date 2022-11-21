from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def add(self, value):
        raise NotImplementedError

    @abstractmethod
    def get(self, id):
        raise NotImplementedError
