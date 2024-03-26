import dash_mantine_components as dmc


class AccuracyRadioGroup(dmc.RadioGroup):
    def __init__(self, component_id: str):
        super().__init__([
            dmc.RadioGroup(
                id=component_id,
                label='C точностью',
                children=[
                    dmc.Radio('Любая', 'any'),
                    dmc.Radio('100%', '100'),
                    dmc.Radio('70-90%', '70-90'),
                    dmc.Radio('<10%', '<50'),
                    dmc.Radio('0-10%', '0')
                ],
                value='any',
                orientation='vertical'
            )
        ])
