import os
from abc import ABC, abstractmethod

import meshio

from . import datas


class File(ABC):
    def __init__(self, path):
        """Constructor loads headers and metadata"""
        self.path = path
        self.metadata = None
        self.dataCount = 0
        self.data = []

    @abstractmethod
    def print_data_info(self):
        pass

    def get_data(self, id):
        """Load and return the data for the given id."""

        # Initialize self.data with None values if needed
        if len(self.data) != self.dataCount:
            self.data = [None] * self.dataCount

        # Load data if needed
        if self.data[id] is None:
            self.data[id] = self._load_data(id)

        return self.data[id]

    @abstractmethod
    def _load_data(self, id):
        """Load and return data for the given id"""
        pass


class Vtu(File):
    def __init__(self, path):
        super().__init__(path)
        self.metadata = meshio.read(path)
        self.dataCount = 1

    def print_data_info(self):
        print("0: meshio")

    def _load_data(self, id):
        return datas.Meshio(self.metadata)


def load(path):
    # get file extension
    extension = os.path.splitext(path)[1]

    if extension == ".vtu":
        return Vtu(path)

    else:
        raise Exception("File type not supported")
