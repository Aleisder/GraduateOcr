import dash_mantine_components as dmc


class SelectLanguage(dmc.RadioGroup):
    def __init__(self, component_id: str):
        super().__init__([
            dmc.RadioGroup(
                id=component_id,
                children=[
                    dmc.Radio('English', 'eng'),
                    dmc.Radio('Japanese', 'jpn')
                ],
                label='Выберите язык документа',
                orientation='vertical'
            )
        ])
