import importlib
import inspect
import json
import hashlib
import tempfile
import os
from io import BytesIO
from html2image import Html2Image
from .frame_context import Action, ActionResult, HtmlView, ImageView, ImageFile
from .frame_app_loader import FrameAppLoader, FrameProgram
from .farcaster_client import FarcasterClient


class FrameAppRunner:
    def __init__(self, app, host, size=None, temp_dir=None, fake=None):
        if size == None:
            size = (640, 336)
        self.program = FrameAppLoader.load(app, host)
        self.temp_dir = temp_dir if temp_dir else tempfile.gettempdir()
        self.hti = Html2Image(output_path=self.temp_dir, size=size)
        self.fake_cast, self.fake_caster = fake if fake else (
            "0x07fd3fc61dbc5f0fdbdbec3f3fb70ea9a3eb4435", 3)

    def gen_frame_meta(self, page, action, action_result):
        frame = {}
        cat, path = self._gen_frame_view_in_advance(
            page, action, action_result)
        if cat == "cached":
            image_url = f'{self.program.uri}/view/{path}'
        elif cat == "static":
            image_url = f'{self.program.uri}/static/{path}'
        click_url = f'{self.program.uri}/{page}/click'
        frame["fc:frame"] = "vNext"
        frame["fc:frame:image"] = image_url
        frame["fc:frame:post_url"] = click_url
        buttons = self.program.pages[page]["btns"]
        for idx, button in enumerate(buttons):
            frame[f"fc:frame:button:{idx+1}"] = button[0]
        return frame

    def gen_og_meta(self):
        meta = {}
        meta["og:url"] = self.program.uri
        meta["og:title"] = self.program.name
        meta["og:description"] = self.program.description
        meta["og:image"] = self.program.image
        meta["og:image:type"] = "image/png"
        return meta

    def start(self):
        page = self.program.start
        action = Action.default()
        og = self.gen_og_meta()
        frame = self.gen_frame_meta(page, action, ActionResult())
        frame |= og
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

        # fake cast https://warpcast.com/~/developers/frames
        if action.cast == "0x0000000000000000000000000000000000000001":
            action.action = post_data["untrustedData"]["buttonIndex"]
            action.cast = self.fake_cast
            action.caster = self.fake_caster

        next_page, action_result = self.program.execute_btn_func(page, action)
        return self.gen_frame_meta(next_page, action, action_result)

    @staticmethod
    def gen_frame_html(metas, template=None):
        if not template:
            template = '''<!DOCTYPE html><html><head>{meta_html}</head><body/></html>'''
        a = []
        for (k, v) in metas.items():
            a.append(FrameAppRunner._meta_tag(k, v))
        meta_html = "\n".join(a)
        html = template.format(meta_html=meta_html)
        return html

    def _gen_frame_view_in_advance(self, page, action, action_result):
        view = self.program.execute_view_func(page, action, action_result)
        print(view)
        if isinstance(view, HtmlView):
            digest = hashlib.sha256(view.html.encode()).hexdigest()
            name = f"{digest}.png"
            path = f"{self.temp_dir}/{digest}.png"
            if not os.path.exists(path):
                self._screenshot(view.html, name, css=view.css)
            return ("cached", name)
        elif isinstance(view, ImageView):
            digest = hashlib.sha256(view.content).hexdigest()
            name = f"{digest}.png"
            path = f"{self.temp_dir}/{digest}.png"
            if not os.path.exists(path):
                with open(path, 'w') as file:
                    file.write(view.content)
            return ("cached", name)
        elif isinstance(view, ImageFile):
            return ("static", view.path)
        else:
            raise Exception("view type not supported")

    def _screenshot(self, html, name, css=None):
        self.hti.screenshot(html_str=html, save_as=name, css_str=css)

    @staticmethod
    def _encode_state(action, action_result):
        return f"{action.encode()}_{action_result.encode()}"

    @staticmethod
    def _decode_state(state):
        a, ar = state.split("_")
        a = Action.decode(a)
        ar = ActionResult.decode(ar)
        return a, ar

    @staticmethod
    def _meta_tag(prop, content):
        return f'<meta property="{prop}" content="{content}" />'
