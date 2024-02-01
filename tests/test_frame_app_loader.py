from sufficient.frames.frame_app_loader import FrameAppLoader
from .frame_apps import gm


class TestFrameAppLoader:
    def test_load_app(self):
        app = FrameAppLoader.load(gm, "http://localhost:3000")
        print(app)
