
from sufficient.frames import HtmlText, ImageBinary, Action, ActionResult


class App:
    name = "Degen"
    description = "An example frame app"
    logo = "http://a.b.com/logo.png"
    uri = "http://a.b.com"
    start = "PageHome"


class PageHome:
    def view(self, action: Action, result: ActionResult):
        html = f"""<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://cdn.rawgit.com/Chalarangelo/mini.css/v3.0.1/dist/mini-default.min.css" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <body>
    <div class="row">
      <img src="image.png" alt="Image description"/>
      <div class="card">{App.desc}</div>
      <div class="card">This is a basic card with some sample content.</div>
      <blockquote cite="www.quotation.source">This is some text quoted from elsewhere.</blockquote>
    </div>
  </body>
</html>
"""
        return HtmlText(html)

    def btn_be_a_degentlemen(self, action: Action):
        return "PageDegentlemen"


class PageDegentlemen:
    def view(self, action: Action, result: ActionResult):
        canvas = Image.new('RGB', (640, 336), 'red')
        l, t = 100, 150
        for r in a:
            img_io = BytesIO(r.value)
            im = Image.open(img_io)
            im = im.resize((60, 60))
            canvas.paste(im, (l, t))
            l += 100

        bio = BytesIO()
        canvas.save(bio, format="PNG")
        return ImageBinary("image/png", bio.getvalue())
