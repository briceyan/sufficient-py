from sufficient.frames import TemplateRender
from .frame_apps import gm as gm_app
import os


class TestTemplateRender:
    def test_main_page_meta(self):
        app_path = gm_app.__file__
        app_dir = os.path.dirname(app_path)
        static_dir = os.path.join(app_dir, "static")
        templates_dir = os.path.join(app_dir,  "templates")
        data_dir = os.path.join(app_dir,  "data")

        tr = TemplateRender(templates_dir)
        result = tr.render_template(
            "greeting.svg", name="a", pfp="http://a.b.c/d.png")
        print(result)
