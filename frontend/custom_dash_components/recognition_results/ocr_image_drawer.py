from dash import html, callback, Output, Input
from dataclasses import dataclass


def generate_id_from_url(url: str) -> str:
    start_index = url.index('image')
    end_index = url.index('.png')
    return url[start_index:end_index]


class OcrPageDrawer(html.Div):
    pass

    # @dataclass
    # class Props:
    #     id: str
    #     url: str
    #     drawer_id: str
    #
    # props = Props
    #
    # def __init__(self, url: str, drawer_id: str):
    #     self.id = generate_id_from_url(url)
    #     self.props.id = self.id
    #     self.props.url = url
    #     self.props.drawer_id = drawer_id
    #
    #     super().__init__([
    #         html.Img(
    #             id=self.id,
    #             src=url,
    #             height=500
    #         )
    #     ])
    #
    # @callback(
    #     Output(props.drawer_id, 'opened'),
    #     Output(props.drawer_id, 'children'),
    #     Input(props.id, 'n_clicks')
    # )
    # def open_drawer(self, n_clicks):
    #     if n_clicks is not None:
    #         return True, html.Img(src=self.id, height=900)
