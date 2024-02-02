import chevron
import json


class Action:
    def __init__(self, cast, caster, actor, action, page=None, button=None):
        self.caster = caster
        self.cast = cast
        self.actor = actor
        self.action = action
        self.set_source(page, button)

    def set_source(self, page, button):
        self.page = page
        self.button = button
        self.source = f"{page}.{button}" if page and button else None

    def __str__(self):
        return f"Action(cast={self.cast}, caster={self.caster}, actor={self.actor}, action={self.action}, page={self.page})"

    @staticmethod
    def default():
        return Action("0x", 0, 0, 0)

    @staticmethod
    def from_untrusted_data(untrusted_data, page):
        cast = untrusted_data["castId"]["hash"]
        caster = untrusted_data["castId"]["fid"]
        actor = untrusted_data["fid"]
        action = untrusted_data["buttonIndex"]
        return Action(cast, caster, actor, action, page)

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
    def __init__(self, **kwargs):
        self.__kwargs__ = kwargs

    def __getattr__(self, name):
        if name != "__kwargs__":
            return self.__kwargs__[name]
        else:
            raise AttributeError()

    def to_kwargs(self):
        return object.__getattribute__(self, "__kwargs__")

    @staticmethod
    def default():
        return ActionResult()

    def __str__(self):
        attrs = [f"{key}={value}" for key, value in sel.kwargs.items()]
        return f"{self.__class__.__name__}({', '.join(attrs)})"


# class ActionResult:
#     def __init__(self, **kwargs):
#         self.errors = errors
#         self.data = data

#     @staticmethod
#     def default():
#         return ActionResult()

#     @staticmethod
#     def decode(hex_data):
#         js_str = bytes.fromhex(hex_data).decode("utf-8")
#         data = json.loads(js_str)
#         ar = ActionResult()
#         if "data" in data:
#             ar.data = data["data"]
#         if "errors" in data:
#             ar.errors = data["errors"]
#         return ar

#     def encode(self):
#         data = {}
#         if self.data:
#             data["data"] = self.data
#         if self.errors:
#             data["errors"] = self.errors
#         return json.dumps(data).encode().hex()

#     def __str__(self):
#         return f"ActionResult(data={self.data}, errors={self.errors})"


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
    def from_template(name, attr_dict):
        return SvgImageView("template", [name, attr_dict])

    def get_content(self, static_dir, template_render):
        if self.source == "memory":
            return self.data[0]
        elif self.source == "file":
            return open(f"{static_dir}/{self.data[0]}", "r").read()
        elif self.source == "template":
            return template_render.render_template(self.data[0], **self.data[1].to_kwargs())
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
    def from_function(func, attr_dict):
        return BinaryImageView("function", [func, attr_dict])

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


class TemplateRender:
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir

    def render_template(self, template_name, **kwargs):
        path = f"{self.templates_dir}/{template_name}"
        with open(path, 'r') as f:
            return chevron.render(f, kwargs)
