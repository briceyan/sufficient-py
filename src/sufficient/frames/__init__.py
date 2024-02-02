from .frame_context import BinaryImageView, SvgImageView, Action, ActionResult, TemplateRender
from .farcaster_client import FarcasterClient
from .frame_app_runner import FrameAppRunner


def ImageFile(file):
    return BinaryImageView.from_file(file)


def ImageBinary(data):
    return BinaryImageView.from_bytes(data)


def SvgFile(file):
    return SvgImageView.from_file(file)


def SvgTemplate(name_, result):
    return SvgImageView.from_template(name_, result)
