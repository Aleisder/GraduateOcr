from dash import html


class TextContainer(html.Div):
    def __init__(self, component_id: str):
        super().__init__([
            html.Div(
                id=component_id,
                className='recognized-text-container'
            )
        ])
