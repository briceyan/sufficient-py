
from sufficient.frames import *


class App:
    name = "Hello Frames"
    description = "An example frame app"
    logo = "http://a.b.com/logo.png"
    uri = "http://a.b.com"
    start = "PageHome"


class PageHome:
    def view(self, action: Action, result: ActionResult):
        html = f"""<div>
<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
<p>This is a paragraph.</p>
</div>
"""
        return HtmlText(html)

    def btn_home_1(self, action: Action):
        return "PageHome"

    def btn_home2(self, action: Action):
        return "PageHome"


class PageNext:
    def view(self, action: Action, result: ActionResult):
        print(action.caster, action.cast)
        c = FarcasterClient()
        u = c.get_user(action.caster)
        print(u)
        html = f"""<div>
<h1>This is a Heading</h1>
<p>This is a paragraph.</p>
<p>This is a abc.</p>
<p>This is a abc.</p>
<img src="{u["pfp_url"]}"/>
<div class="card">cast={action.cast}</div>
<div class="card">caster={action.caster}</div>
</div>
"""
        return HtmlText(html)

    def btn_next_button1(self, action: Action):
        return "PageNext"

    def btn_next_button2(self, action: Action):
        return "PageHome"
