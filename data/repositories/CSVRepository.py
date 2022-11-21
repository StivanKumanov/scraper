from services.repositories.BaseRepository import BaseRepository
import csv


class CSVRepository(BaseRepository):

    def add(self, value):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError


