import json
from jinja2 import Environment, FileSystemLoader, select_autoescape


class Action:
    def __init__(self, cast, caster, actor, action, page=None):
        self.caster = caster
        self.cast = cast
        self.actor = actor
        self.action = action
        self.page = page

    def __str__(self):
        return f"Action(cast={self.cast}, caster={self.caster}, actor={self.actor}, action={self.action}, page={self.page})"

    @staticmethod
    def default():
        return Action("0x", 0, 0, 0)

    @staticmethod
    def from_verified_message(message, page):
        cast = message["data"]["frameActionBody"]["castId"]["hash"]
        caster = message["data"]["frameActionBody"]["castId"]["fid"]
        actor = message["data"]["fid"]
        action = message["data"]["frameActionBody"]["buttonIndex"]
        return Action(cast, caster, actor, action, page)

    # @staticmethod
    # def from_neynar_validated_frame_action(vfa):
    #     print(vfa)
    #     if "cast" in vfa:
    #         cast = vfa["cast"]["hash"]
    #         caster = vfa["cast"]["author"]["fid"]
    #         extra = {"actor_user": vfa["interactor"],
    #                  "caster_user":  vfa["cast"]["author"],
    #                  "cast_info": {"text":  vfa["cast"]["text"], "timestamp": vfa["cast"]["timestamp"]},
    #                  "likes": vfa["cast"]["reactions"]["likes"],
    #                  "recasts": vfa["cast"]["reactions"]["recasts"],
    #                  "replies": vfa["cast"]["replies"]}
    #     else:
    #         cast = "0x"
    #         caster = 0
    #         extra = None

    #     actor = vfa["interactor"]["fid"]
    #     action = vfa["tapped_button"]["index"]
    #     return Action(cast, caster, actor, action, extra=extra)

    @staticmethod
    def decode(hex_data):
        js_str = bytes.fromhex(hex_data).decode("utf-8")
        data = json.loads(js_str)
        cast, caster, actor, action = data
        return Action(cast, caster, actor, action)

    def encode(self):
        data = [self.cast, self.caster, self.actor, self.action]
        return json.dumps(data).encode().hex()


class ActionResult:
    def __init__(self, data=None, errors=None):
        self.errors = errors
        self.data = data

    @staticmethod
    def default():
        return ActionResult()

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

    def __str__(self):
        return f"ActionResult(data={self.data}, errors={self.errors})"


class TemplateRender:
    def __init__(self, templates_dir):
        loader = FileSystemLoader(searchpath=templates_dir),
        autoesc = select_autoescape(['xml', 'html', 'svg'])
        self.env = Environment(loader=loader, autoescape=autoesc)

    def render_template(self, name, **kwargs):
        template = env.get_template(name)
        return template.render(**kwargs)


class SvgImageView:
    def __init__(self, source, data):
        self.source = source
        self.data = data

    @staticmethod
    def from_string(content):
        return SvgImageView("memory", [content])

    @staticmethod
    def from_file(name):
        return SvgImageView("file", [name])

    @staticmethod
    def from_template(name, **kwargs):
        return SvgImageView("template", [name, kwargs])

    def get_content(self, static_dir, template_render):
        if self.source == "memory":
            return self.data[0]
        elif self.source == "file":
            return open(f"{static_dir}/{self.data[0]}", "r").read()
        elif self.source == "template":
            return template_render.render_template(self.data[0], **self.data[1])
        else:
            raise Exception("invalid source type")


class BinaryImageView:
    def __init__(self, source, data):
        self.source = source
        self.data = data

    @staticmethod
    def from_file(name):
        return BinaryImageView("file", [name])

    @staticmethod
    def from_bytes(content):
        return BinaryImageView("memory", [content])

    @staticmethod
    def from_function(func, **kwargs):
        return BinaryImageView("function", [func, kwargs])

    def get_content(self, static_dir):
        if self.source == "memory":
            return self.data[0]
        elif self.source == "file":
            return open(f"{static_dir}/{self.data[0]}", "rb").read()
        elif self.source == "function":
            raise Exception("not implemented")
            # return template_render.render_template(self.data[0], **self.data[1])
        else:
            raise Exception("invalid source type")

    # def __str__(self):
    #     return f"ImageFile(path={self.path})"
