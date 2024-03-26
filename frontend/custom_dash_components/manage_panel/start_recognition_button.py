import dash_mantine_components as dmc
from dash_iconify import DashIconify


class StartRecognitionButton(dmc.Button):
    def __init__(self, component_id: str):
        super().__init__([
            dmc.Button(
                id=component_id,
                children='Начать распознание',
                rightIcon=DashIconify(icon='material-symbols:search')
            )
        ])
