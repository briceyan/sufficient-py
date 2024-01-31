import json


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


class HtmlView:
    def __init__(self, html, css=None):
        self.html = html
        self.css = css

    def __str__(self):
        return f"HtmlView(html={len(self.html)}B, css={len(self.css) if self.css else 0}B)"


class ImageView:
    def __init__(self, content_type, content):
        self.content_type = content_type
        self.content = content

    def __str__(self):
        return f"ImageView(content_type={self.content_type}, content={len(self.content)}B)"


class ImageFile:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f"ImageFile(path={self.path})"
