from sufficient.frames.frame_app_loader import FrameAppLoader
from sufficient.examples import degen
import os


class TestFrameAppLoader:
    def test_load_app(self):
        app = FrameAppLoader.load(degen)
        print(app)
