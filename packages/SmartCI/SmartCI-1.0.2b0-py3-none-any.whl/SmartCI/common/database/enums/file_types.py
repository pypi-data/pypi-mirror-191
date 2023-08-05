from enum import Enum


class FileTypes(Enum):
    Code = 'code'
    Test = 'test'
    INIT = 'init'

    @classmethod
    def values(cls):
        return {
            'code': 'code',
            'test': 'test',
            'init': 'init'
        }

    def __dict__(self):
        return {
            'code': 'code',
            'test': 'test',
            'init': 'init'
        }