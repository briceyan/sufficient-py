from sufficient.frames import *


class App:
    name = "Sufficient-py"
    description = "A framework for creating Frame apps in an intuitive and declarative manner"
    image = "{uri}/static/home.png"
    uri = "{uri}"
    start = "PageHome"


class PageHome:
    def view(self, action: Action, result: ActionResult):
        return ImageFile("home.png")

    def btn_features(self, action: Action):
        c = FarcasterClient()
        actor_user = c.neynar_get_user(action.actor)
        return "PageDemo", ActionResult(data=actor_user)

    def btn_concepts(self, action: Action):
        return "PageConcepts"


class PageDemo:
    def view(self, action: Action, result: ActionResult):
        if action.page == "PageDemo":
            if action.action == 1:
                html = self._show_reactions(result)
            elif action.action == 2:
                html = self._show_token_infos(result)
            elif action.action == 3:
                html = self._show_render_methods(result)
        else:
            html = self._show_greeting(result)
        return HtmlView(html, css=CSS)

    def btn_get_reactions(self, action: Action):
        c = FarcasterClient()
        cast_actions = c.neynar_get_cast_actions(action.cast, action.actor)
        return "PageDemo", ActionResult(data=cast_actions)

    def btn_get_tokens(self, action: Action):
        return "PageDemo"

    def btn_render_methods(self, action: Action):
        return "PageDemo"

    def btn_declarative(self, action: Action):
        return "PageConcepts"

    def _show_greeting(self, result: ActionResult):
        actor_user = result.data
        html = f"""
<div class="center">
  <img src="{actor_user["pfp_url"]}" width="100" height="100"/>
  <h3>gm, {actor_user["display_name"]}</h3>
  <p class="medium">Sufficient is a framework for creating Frame apps in an intuitive and declarative manner.</p>
  <p class="medium">Click buttons to learn about features of sufficient.</p>
</div>
"""
        return html

    def _show_reactions(self, result: ActionResult):
        cast_actions = result.data
        likes = cast_actions["reactions"]["likes"]
        recasts = cast_actions["reactions"]["recasts"]
        num_replies = cast_actions["replies"]["count"]
        html = f"""
<div class="center">
  <h2>Get Reactions</h2>
  <div class="medium">
  <p>
   Farcaster data validation and acquisition are currently being accomplished by encapsulating a few APIs from Hub and Neynar.
  </p>
  <p>
    Recast or like to see number changes
  </p>
  </div>
  <ul class="small">
    <li>#likes: {len(likes)}</li>
    <li>#recasts: {len(recasts)}</li>
    <li>#replies: {num_replies}</li>
  </ul>
</div>
"""
        return html

    def _show_token_infos(self, result: ActionResult):
        html = """
<div class="center">
  <h2>Get Tokens</h2>
  <p class="medium">
   Integration with other APIs can enable on-chain information queries, to be implemented
  </p>
</div>
"""
        return html

    def _show_render_methods(self, result: ActionResult):
        html = """
<div class="center">
  <h2>Render Methods</h2>
  <p class="medium">
    Sufficient library offers flexible image processing options beyond HTML/CSS and static image files.
  </p>
  <ul class="small">
    <li>HTML + CSS</li>
    <li>Static image file</li>    
    <li>Image processing utils</li>
  </ul>
</div>
"""
        return html


class PageConcepts:
    def view(self, action: Action, result: ActionResult):
        if action.page == "PageConcepts":
            if action.action == 1:
                return ImageFile("page.png")
            elif action.action == 2:
                return ImageFile("view.png")
            elif action.action == 3:
                return ImageFile("action.png")
        else:
            return HtmlView(self._show_concepts(result), css=CSS)

    def btn_page(self, action: Action):
        return "PageConcepts"

    def btn_view(self, action: Action):
        return "PageConcepts"

    def btn_action(self, action: Action):
        return "PageConcepts"

    def btn_contribute(self, action: Action):
        return "PageContribute"

    def _show_concepts(self, result: ActionResult):
        html = """
<div class="center">
  <h2>Declarative</h2>
  <p></>
  <ul class="small">
    <li>app = (name, description, logo, uri, pages)</li>
    <li>page = (view, btn_1, btn_2, ...)</li>
    <li>view = static file | html | udf </li>
    <li>btn_i = (handler, next_page_name)</li>
  </ul>
  <p></>
  <p>Click buttons to learn</>
</div>
"""
        return html


class PageContribute:
    def view(self, action: Action, result: ActionResult):
        return ImageFile("contribute.png")

    def btn_back_home(self, action: Action):
        return "PageHome"


CSS = """
  .center {
    width: 100%;
    padding: 16px;
    margin: auto;
    text-align: center;
  }
  .medium {
    width: 70%;    
    text-align: left;
    margin: auto;
  }
  .small {
    width: 50%;
    background-color: lightgrey;
    text-align: left;
    margin: auto;
  }
"""
