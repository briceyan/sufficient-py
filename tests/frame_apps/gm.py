from sufficient.frames import *


class App:
    name = "Gm World"
    description = "Say hi to the world of frames"
    image = "{uri}/static/home.svg"
    uri = "{uri}"
    start = "PageHome"


class PageHome:
    def view(self, action: Action, result: ActionResult):
        return SvgImageView.from_string(HOME_VIEW)

    def btn_next_page(self, action: Action):
        return "PageNext"

    def btn_stay_here(self, action: Action):
        return "PageHome"


class PageNext:
    def view(self, action: Action, result: ActionResult):
        return SvgImageView.from_string(NEXT_VIEW)

    def btn_back_home(self, action: Action):
        return "PageHome"

    def btn_stay_here(self, action: Action):
        return "PageNext"


HOME_VIEW = """
<svg width="640" height="336" viewBox="0 0 640 336" xmlns="http://www.w3.org/2000/svg" >
  <text>
    Page Home
  </text>
  <style>
    <![CDATA[
      text{
        dominant-baseline: hanging;
        font: 28px Verdana, Helvetica, Arial, sans-serif;
      }
    ]]>
  </style>
</svg>
"""

NEXT_VIEW = """
<svg  width="640" height="336" viewBox="0 0 640 336"  xmlns="http://www.w3.org/2000/svg" >
  <text>
    Page Next
  </text>
  <style>
    <![CDATA[
      text{
        dominant-baseline: hanging;
        font: 28px Verdana, Helvetica, Arial, sans-serif;
      }
    ]]>
  </style>
</svg>
"""
