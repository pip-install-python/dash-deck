import base64
from io import BytesIO
import os
import time

import dash
from dash import dcc, html, Input, Output
from PIL import Image


def pil_to_b64(im, ext="jpeg"):
    if ext == "jpg":
        ext = "jpeg"

    if ext == "jpeg" and im.mode in ("RGBA", "LA"):
        background = Image.new(im.mode[:-1], im.size, (255, 255, 255))
        background.paste(im, im.split()[-1])
        im = background

    buffer = BytesIO()
    im.save(buffer, format=ext)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return f"data:image/{ext};base64, " + encoded


def build_app(imgs):
    app = dash.Dash(__name__)
    app.layout = html.Div(
        [html.Img(id="display"), dcc.Location(id="url", refresh=False)]
    )

    @app.callback(Output("display", "src"), [Input("url", "pathname")])
    def update_image(url):
        if url in [None, "/"]:
            return dash.no_update
        return pil_to_b64(imgs[url.strip("/")], ext="png")

    return app


def test_percy(dash_duo):
    img_dir = "/tmp/dash_artifacts/"
    imgs = {
        fname.replace(".png", ".py"): Image.open(os.path.join(img_dir, fname))
        for fname in os.listdir(img_dir)
    }

    app = build_app(imgs)
    dash_duo.start_server(app)

    for name in imgs:
        dash_duo.wait_for_page(url=dash_duo.server_url + "/" + name)
        time.sleep(2)
        dash_duo.percy_snapshot(name)
