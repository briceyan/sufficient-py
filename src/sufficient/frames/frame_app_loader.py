import inflection
import inspect
from .frame_context import Action, ActionResult


class FrameProgram:
    def __init__(self, name, desc, image, uri, start, pages):
        self.name = name
        self.description = desc
        self.image = image
        self.uri = uri
        self.start = start
        self.pages = pages

    def get_page_class(self, page):
        return self.pages[page]["class"]

    def get_view_func(self, page):
        return self.pages[page]["view"]

    def get_btn_info(self, page, btn_idx):
        btn_idx_saved, btn_name, btn_func, btn_display_name = self.pages[
            page]["btns"][btn_idx - 1]
        if btn_idx_saved != btn_idx:
            raise Exception("internal error: btn idx mismatch")
        return btn_idx, btn_name, btn_func, btn_display_name

    def execute_view_func(self, page, action, result):
        clz = self.pages[page]["class"]
        func = self.pages[page]["view"]
        return func(clz(), action, result)

    def execute_btn_func(self, page, action):
        btn_idx, btn_name, btn_func, btn_display_name = self.get_btn_info(
            page, action.action)
        action.set_source(page, btn_name)
        clz = self.pages[page]["class"]
        r = btn_func(clz(), action)
        if btn_name.startswith("btn_"):
            if isinstance(r, tuple):
                next_page, result = r
            else:
                next_page, result = r, ActionResult()
        elif btn_name.startswith("goto_"):
            redirect_url = r
            next_page, result = None, ActionResult(redirect_url=redirect_url)
        else:
            raise Exception("internal error: unexpected btn name")
        return next_page, result


class FrameAppLoader:
    @staticmethod
    def load(app, host):
        app_class = getattr(app, "App")
        name = getattr(app_class, "name")
        desc = getattr(app_class, "description")
        image = getattr(app_class, "image")
        uri = getattr(app_class, "uri")
        start = getattr(app_class, "start")

        uri = str(uri).format(uri=host)
        image = str(image).format(uri=host)
        pages = FrameAppLoader.compile_pages(app)
        return FrameProgram(name, desc, image, uri, start, pages)

    @staticmethod
    def compile_pages(app):
        pages = {}
        page_names = list(
            filter(lambda n: not n.startswith("_"), vars(app)))
        for page_name in page_names:
            page_class = getattr(app, page_name)
            if inspect.isclass(page_class) and page_name.startswith("Page"):
                page_buttons = []
                page_image = None
                input_label = None
                for method_name, method_object in FrameAppLoader.get_members_in_order(page_class):
                    if not inspect.isfunction(method_object):
                        continue
                    if method_name.startswith("btn_"):
                        btn_display_name = inflection.humanize(method_name[4:])
                        btn_idx = len(page_buttons) + 1
                        page_buttons.append(
                            (btn_idx, method_name, method_object, btn_display_name))
                    elif method_name.startswith("goto_"):
                        btn_display_name = inflection.humanize(method_name[5:])
                        btn_idx = len(page_buttons) + 1
                        page_buttons.append(
                            (btn_idx, method_name, method_object, btn_display_name))
                    elif method_name.startswith("input_"):
                        input_label = inflection.humanize(method_name[6:])
                    elif method_name == "view":
                        page_image = method_object
                pages[page_name] = {}
                pages[page_name]["class"] = page_class
                pages[page_name]["btns"] = page_buttons
                pages[page_name]["input"] = input_label
                pages[page_name]["view"] = page_image
        return pages

    @staticmethod
    def get_members_in_order(o):
        r = []
        names = filter(lambda n: not n.startswith("_"), vars(o))
        for name in names:
            r.append((name, getattr(o, name)))
        return r
