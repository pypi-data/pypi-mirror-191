from abc import ABC

from . import viewerBackends


# Define decorator that checks if Viewer's backend matches current backend
def check_backend(func):
    def wrapper(self, *args, **kwargs):
        if self.backend is not viewerBackends.current_backend:
            raise RuntimeError(
                "Viewer's backend does not match current"
                " backend. Create a new Viewer instance."
            )
        return func(self, *args, **kwargs)

    return wrapper


class Viewer(ABC):
    def __init__(self):
        pass


class PyvistaPlotter(Viewer):
    def __init__(self):
        super().__init__()
        self.backend = viewerBackends.current_backend
        self.plotter = self.backend.get_pyvista_plotter()

    @check_backend
    def add_mesh(self, data, *args, **kwargs):
        self.backend.add_mesh_pyvista(data, self.plotter, *args, **kwargs)

    @check_backend
    def add_points(self, data, *args, **kwargs):
        self.backend.add_points_pyvista(data, self.plotter, *args, **kwargs)

    @check_backend
    def show(self):
        self.backend.show_pyvista(self.plotter)
