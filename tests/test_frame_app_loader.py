from sufficient.frames.frame_app_loader import FrameAppLoader
from sufficient.examples.gm.frame import app
import os


class TestFrameAppLoader:
    def test_load_app(self):
        program = FrameAppLoader.load(app, "http://localhost:3000")
        print(program)
