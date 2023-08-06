from .simulator import main as simulator
from .demo import main as demo
from .arbiter import PyCar
import pyglet
from threading import Thread

pycar_handle = PyCar()
sim_window = simulator.Window(pycar_handle)
#demo.run(pycar_handle)
demo_window = demo.Window(pycar_handle)
pyglet.app.run()
