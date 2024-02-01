import importlib
import inspect
import json
import hashlib
import tempfile
import os
from io import BytesIO
from .frame_context import Action, ActionResult, SvgImageView, BinaryImageView, TemplateRender
from .frame_app_loader import FrameAppLoader, FrameProgram
from .farcaster_client import FarcasterClient


class FrameAppRunner:
    def __init__(self, app, static_dir, templates_dir, data_dir=None, size=None, fake=None):
        self.program = FrameAppLoader.load(app, "host")
        self.data_dir = data_dir if data_dir else tempfile.gettempdir()
        self.static_dir = static_dir
        self.templates_dir = templates_dir
        self.size = size if size else (640, 336)
        self.fake_cast, self.fake_caster = fake if fake else (
            "0x07fd3fc61dbc5f0fdbdbec3f3fb70ea9a3eb4435", 3)
        self.template_render = TemplateRender(self.templates_dir)

    def start(self):
        frame = self._gen_frame_meta(
            self.program.start, Action.default(), ActionResult())
        return frame

    def click(self, page, post_data):
        if "trustedData" in post_data:
            c = FarcasterClient()
            verified = c.hub_verify_message(
                post_data["trustedData"]["messageBytes"])
            action = Action.from_verified_message(verified, page)
        elif "untrustedData" in post_data:
            d = post_data["untrustedData"]
            action = Action(d["castId"]["fid"], d["castId"]
                            ["hash"], d["fid"], d["buttonIndex"], page)

        # fake cast by https://warpcast.com/~/developers/frames
        if action.cast == "0x0000000000000000000000000000000000000001":
            action.action = post_data["untrustedData"]["buttonIndex"]
            action.cast = self.fake_cast
            action.caster = self.fake_caster

        next_page, action_result = self.program.execute_btn_func(page, action)
        return self._gen_frame_meta(next_page, action, action_result)

    def _gen_frame_meta(self, page, action, action_result):
        frame = {}
        warmed, path = self._warm_frame_view(page, action, action_result)
        if warmed:
            image_url = f'/view/{path}'
        else:
            image_url = f'/static/{path}'
        click_url = f'/{page}/click'
        frame["fc:frame"] = "vNext"
        frame["fc:frame:image"] = image_url
        frame["fc:frame:post_url"] = click_url
        buttons = self.program.pages[page]["btns"]
        for idx, button in enumerate(buttons):
            frame[f"fc:frame:button:{idx+1}"] = button[0]
        return frame

    def _warm_frame_view(self, page, action, action_result):
        view = self.program.execute_view_func(page, action, action_result)
        saved, name = self.save_view_content(
            view, self.template_render, self.static_dir, self.data_dir)
        return saved, name

    @staticmethod
    def save_if_not_exist(content, ext, data_dir):
        digest = hashlib.sha256(content).hexdigest()
        name, path = f"{digest}{ext}", f"{data_dir}/{digest}{ext}"
        if not os.path.exists(path):
            with open(path, 'wb') as file:
                file.write(content)
        return name

    @staticmethod
    def save_view_content(view, template_render, static_dir, data_dir):
        if isinstance(view, SvgImageView):
            if view.source == "file":
                return (False, view.data[0])
            else:
                content = view.get_content(static_dir, template_render)
                name = FrameAppRunner.save_if_not_exist(
                    content.encode(), ".svg", data_dir)
                return (True, name)
        elif isinstance(view, BinaryImageView):
            if view.source == "file":
                return (False, view.data[0])
            else:
                content = view.get_content(static_dir)
                name = FrameAppRunner.save_if_not_exist(
                    content, ".png", data_dir)
                return (True, name)
        else:
            raise Exception("unsupported view type")

    def gen_frame_html(self, frame, host, template=None, og=False):
        host = host.rstrip("/")
        if not template:
            template = '''<!DOCTYPE html><html><head>{meta_html}</head><body/></html>'''
        a = []
        if og:
            og_metas = FrameAppRunner.gen_og_meta(self.program)
            for (k, v) in og_metas.items():
                if k == "og:image":
                    v = str(v).format(uri=host)
                a.append(FrameAppRunner._meta_tag(k, v))
        for (k, v) in frame.items():
            if k == "fc:frame:image" or k == "fc:frame:post_url":
                v = host + v
            a.append(FrameAppRunner._meta_tag(k, v))
        meta_html = "\n".join(a)
        html = template.format(meta_html=meta_html)
        return html

    @staticmethod
    def gen_og_meta(program):
        meta = {}
        meta["og:url"] = program.uri
        meta["og:title"] = program.name
        meta["og:description"] = program.description
        meta["og:image"] = program.image
        meta["og:image:type"] = "image/png"
        return meta

    @staticmethod
    def _meta_tag(k, v):
        return f'<meta property="{k}" content="{v}" />'

    # def _screenshot(self, html, name, css=None):
    #     self.hti.screenshot(html_str=html, save_as=name, css_str=css)

    # @staticmethod
    # def _encode_state(action, action_result):
    #     return f"{action.encode()}_{action_result.encode()}"

    # @staticmethod
    # def _decode_state(state):
    #     a, ar = state.split("_")
    #     a = Action.decode(a)
    #     ar = ActionResult.decode(ar)
    #     return a, ar
