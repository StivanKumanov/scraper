from services.repositories.BaseRepository import BaseRepository


class ExcelRepository(BaseRepository):

    def add(self, value):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError
