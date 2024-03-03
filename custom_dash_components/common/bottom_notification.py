import dash_mantine_components as dmc
from dash_iconify import DashIconify


class BottomNotification(dmc.Notification):
    props = dict()

    def __init__(self, title: str, message: str, icon: str):
        super().__init__([
            dmc.Notification(
                id='notification',
                action='show',
                title=title,
                message=message,
                icon=DashIconify(icon=icon),
                styles={
                    'body': {'width': '100%'},
                    'title': {'fontSize': '36sp'}
                }
            )
        ])
