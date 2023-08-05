from abc import ABC, abstractmethod

import pyvista as pv

from .singleton import Singleton


class Converter(ABC, metaclass=Singleton):
    def __init__(self):
        pass

    @abstractmethod
    def convert(self, internal_data):
        pass


class Same(Converter):
    def __init__(self):
        super().__init__()

    def convert(self, internal_data):
        return internal_data


class MeshioToPyvista(Converter):
    def __init__(self):
        super().__init__()

    def convert(self, internal_data):
        return pv.from_meshio(internal_data)
