import importlib
from html2image import Html2Image
import inspect
import json
from io import BytesIO
from .frame_context import Action, ActionResult, HtmlText, ImageBinary
from .frame_app_loader import FrameAppLoader
from .farcaster_client import FarcasterClient
import tempfile
import os


class FrameAppRunner:
    def __init__(self, app, screenshot_dir=None):
        self._program = FrameAppLoader.load(app)
        self._screenshot_dir = screenshot_dir if screenshot_dir else tempfile.gettempdir()
        self._hti = Html2Image(output_path=self._screenshot_dir, size=(640, 336))

    def to_picture(self, page, state):
        action, action_result = self._decode_state(state)
        print(page, action, action_result)
        view_result = self._program.excute_view_func(
            page, action, action_result)
        if isinstance(view_result, HtmlText):
            return ImageBinary("image/png", self._html_to_image(view_result.html))
        elif isinstance(view_result, ImageBinary):
            return view_result
        else:
            raise Exception("unsupported view content")

    def to_frame(self, page, action, action_result):

        frame = {}
        state = self._encode_state(action, action_result)
        image_url = f'{self._program.uri}/{page}/image/{state}'
        click_url = f'{self._program.uri}/{page}/click'
        frame["fc:frame"] = "vNext"
        frame["fc:frame:image"] = image_url
        frame["fc:frame:post_url"] = click_url
        buttons = self._program.pages[page]["btns"]
        for idx, button in enumerate(buttons):
            frame[f"fc:frame:button:{idx+1}"] = button[0]
        return frame

    def to_open_graph(self):
        meta = {}
        meta["og:title"] = self._program.name
        meta["og:url"] = self._program.uri
        meta["og:image"] = self._program.logo
        meta["og:image:type"] = "image/png"
        return meta

    def on_click(self, page, post_data):
        c = FarcasterClient()
        if "trustedData" not in post_data:
            verified = verify_resp["message"]
        else:
            verified = c.verify_message(
                post_data["trustedData"]["messageBytes"])
        action = Action.from_verified_message(verified)
        next_page, action_result = self._program.excute_btn_func(page, action)
        return self.to_frame(next_page, action, action_result)

    def on_start(self):
        page = self._program.start
        action = Action.start()
        og = self.to_open_graph()
        frame = self.to_frame(page, action, ActionResult())
        frame |= og
        return frame

    @staticmethod
    def _encode_state(action, action_result):
        return f"{action.encode()}_{action_result.encode()}"

    @staticmethod
    def _decode_state(state):
        a, ar = state.split("_")
        a = Action.decode(a)
        ar = ActionResult.decode(ar)
        return a, ar

    def _ogm(self, prop, content):
        return f'<meta property="{prop}" content="{content}" />'

    def _html_to_image(self, html):
        bio = BytesIO()
        tf = tempfile.NamedTemporaryFile(dir=self._screenshot_dir, suffix=".png")
        base_name = os.path.basename(tf.name)
        paths = self._hti.screenshot(html_str=html, save_as=base_name)
        print("tf.name", tf.name)
        print("paths", paths)
        return open(paths[0], "rb").read()


verify_resp = {
    "valid": True,
    "message": {
        "data": {
            "type": "MESSAGE_TYPE_FRAME_ACTION",
            "fid": 21828,
            "timestamp": 96774342,
            "network": "FARCASTER_NETWORK_MAINNET",
            "frameActionBody": {
                "url": "aHR0cDovL2V4YW1wbGUuY29t",
                "buttonIndex": 1,
                "castId": {
                    "fid": 21828,
                    "hash": "0x1fd48ddc9d5910046acfa5e1b91d253763e320c3"
                }
            }
        },
        "hash": "0x230a1291ae8e220bf9173d9090716981402bdd3d",
        "hashScheme": "HASH_SCHEME_BLAKE3",
        "signature": "8IyQdIav4cMxFWW3onwfABHHS9IroWer6Lowo16AjL6uZ0rve3TTFhxhhuSOPMTYQ8XsncHc6ca3FUetzALJDA==",
        "signer": "0x196a70ac9847d59e039d0cfcf0cde1adac12f5fb447bb53334d67ab18246306c"
    }
}
