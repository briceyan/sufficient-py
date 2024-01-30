import json


class FrameProgram:
    def __init__(self, name, desc, logo, uri, start, pages):
        self.name = name
        self.description = desc
        self.logo = logo
        self.uri = uri
        self.start = start
        self.pages = pages

    def get_page_class(self, page):
        return self.pages[page]["class"]

    def get_view_function(self, page):
        return self.pages[page]["view"]

    def excute_view_func(self, page, action, result):
        clz = self.pages[page]["class"]
        func = self.pages[page]["view"]
        return func(clz(), action, result)

    def excute_btn_func(self, page, action):
        clz = self.pages[page]["class"]
        btn_idx = action.action - 1
        btn_name, btn_func = self.pages[page]["btns"][btn_idx]
        r = btn_func(clz(), action)
        if isinstance(r, tuple):
            next_page, result = r
        else:
            next_page, result = r, ActionResult()
        return next_page, result


class Action:
    def __init__(self, caster, cast, actor, action):
        print("__init__", caster, cast, actor, action)
        self.caster = caster
        self.cast = cast
        self.actor = actor
        self.action = action

    def __str__(self):
        return f"cast={self.cast}, caster={self.caster}"

    @staticmethod
    def start():
        return Action("", 0, 0, 0)

    @staticmethod
    def from_verified_message(message):
        cast = message["data"]["frameActionBody"]["castId"]["hash"]
        caster = message["data"]["frameActionBody"]["castId"]["fid"]
        actor = message["data"]["fid"]
        action = message["data"]["frameActionBody"]["buttonIndex"]
        return Action(caster, cast, actor, action)

    @staticmethod
    def decode(hex_data):
        js_str = bytes.fromhex(hex_data).decode("utf-8")
        data = json.loads(js_str)
        return Action(data["cast"], data["caster"], data["actor"], data["action"])

    def encode(self):
        data = {"cast": self.cast, "caster": self.caster,
                "actor": self.actor, "action": self.action}
        return json.dumps(data).encode().hex()


class ActionResult:
    def __init__(self, data=None, errors=None):
        self.errors = errors
        self.data = data

    @staticmethod
    def decode(hex_data):
        js_str = bytes.fromhex(hex_data).decode("utf-8")
        data = json.loads(js_str)
        ar = ActionResult()
        if "data" in data:
            ar.data = data["data"]
        if "errors" in data:
            ar.errors = data["errors"]
        return ar

    def encode(self):
        data = {}
        if self.data:
            data["data"] = self.data
        if self.errors:
            data["errors"] = self.errors
        return json.dumps(data).encode().hex()


class HtmlText:
    def __init__(self, html, css=None):
        self.html = html
        self.css = css

    def __str__(self):
        return f"HtmlText content: {len(self.html)} bytes"


class ImageBinary:
    def __init__(self, content_type, content):
        self.content_type = content_type
        self.content = content

    def __str__(self):
        return f"ImageBinary content_type: {self.content_type} content: {len(self.content)} bytes"
