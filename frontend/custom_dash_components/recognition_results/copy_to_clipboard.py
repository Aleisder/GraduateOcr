import dash_mantine_components as dmc
import pyperclip
from dash import no_update, State, callback, Output, Input
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify


class CopyClipboardButton(dmc.ActionIcon):
    props = dict()

    def __init__(self, component_id: str, read_from_component_id: str):
        self.props['id'] = component_id
        self.props['read_from'] = read_from_component_id

        super().__init__([
            dmc.ActionIcon(
                id=self.props['id'],
                children=DashIconify(
                    icon='bi:copy',
                    height=18,
                    width=18
                ),
                size=24,
                n_clicks=0,
                radius=5
            )
        ])

        @callback(
            Output(self.props['id'], 'children'),
            Input(self.props['id'], 'n_clicks'),
            State(self.props['read_from'], 'children'),
            prevent_initial_call=True
        )
        def copy_to_clipboard(n_clicks, text):
            if any([n_clicks, text]) is None:
                raise PreventUpdate
            pyperclip.copy(text)
            return no_update
