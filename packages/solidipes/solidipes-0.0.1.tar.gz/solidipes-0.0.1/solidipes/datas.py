from abc import ABC

from . import converters


class Data(ABC):
    def __init__(self, internal_data):
        self.internal_data = internal_data
        self.__converter = converters.Same()
        self.__viewable_data = None
        self.thumbnail = None

    @property
    def viewable_data(self):
        # Convert data if not already converted
        if self.__viewable_data is None:
            self.__viewable_data = self.__converter.convert(self.internal_data)
        return self.__viewable_data


class Meshio(Data):
    def __init__(self, internal_data):
        super().__init__(internal_data)
        self.converter = converters.MeshioToPyvista()
