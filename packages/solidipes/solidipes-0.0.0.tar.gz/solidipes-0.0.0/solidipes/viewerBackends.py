from abc import ABC

import pyvista as pv

from .singleton import Singleton


class ViewerBackend(ABC, metaclass=Singleton):
    def __init__(self):
        pass

    def get_pyvista_plotter(self):
        return pv.Plotter()

    def add_mesh_pyvista(self, data, plotter, *args, **kwargs):
        plotter.add_mesh(data.viewable_data, *args, **kwargs)

    def add_points_pyvista(self, data, plotter, *args, **kwargs):
        plotter.add_points(data.viewable_data, *args, **kwargs)

    def show_pyvista(self, plotter):
        plotter.show()

    def __str__(self):
        return self.__class__.__name__


class Python(ViewerBackend):
    def __init__(self):
        super().__init__()


class JupyterNotebook(ViewerBackend):
    def __init__(self):
        super().__init__()


class Streamlit(ViewerBackend):
    def __init__(self):
        super().__init__()

        # Importing stpyvista here to avoid issues in Jupyter Notebook
        from stpyvista import stpyvista

        self.stpyvista = stpyvista

    def show_pyvista(self, plotter):
        self.stpyvista(plotter)


# Define current backend
current_backend = Python()


def set_backend(backend):
    global current_backend
    if not issubclass(backend, ViewerBackend):
        raise TypeError("backend is not a ViewerBackend")
    current_backend = backend()


# Check if running inside Jupyter Notebook, change backend if so
try:
    shell = get_ipython().__class__.__name__  # type: ignore
    if shell == "ZMQInteractiveShell":
        set_backend(JupyterNotebook)
except NameError:
    pass

# Check if running inside Streamlit, change backend if so
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    if get_script_run_ctx():
        set_backend(Streamlit)
except ModuleNotFoundError:
    pass
