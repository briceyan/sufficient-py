import inflection
import inspect
from .frame_context import FrameProgram


class FrameAppLoader:
    @staticmethod
    def load(app_mod):
        app_class = getattr(app_mod, "App")
        name = getattr(app_class, "name")
        desc = getattr(app_class, "description")
        logo = getattr(app_class, "logo")
        uri = getattr(app_class, "uri")
        start = getattr(app_class, "start")

        pages = {}
        page_names = list(
            filter(lambda n: not n.startswith("_"), vars(app_mod)))
        print(page_names)
        for page_name in page_names:
            page_class = getattr(app_mod, page_name)
            if inspect.isclass(page_class) and page_name.startswith("Page"):
                page_buttons = []
                page_image = None
                for method_name, method_object in FrameAppLoader.get_members_in_order(page_class):
                    if not inspect.isfunction(method_object):
                        continue
                    if method_name.startswith("btn_"):
                        name = inflection.humanize(method_name[4:])
                        page_buttons.append((name, method_object))
                    if method_name == "view":
                        page_image = method_object
                pages[page_name] = {}
                pages[page_name]["class"] = page_class
                pages[page_name]["btns"] = page_buttons
                pages[page_name]["view"] = page_image
        return FrameProgram(name, desc, logo, uri, start, pages)

    @staticmethod
    def get_members_in_order(o):
        r = []
        names = filter(lambda n: not n.startswith("_"), vars(o))
        for name in names:
            r.append((name, getattr(o, name)))
        return r
