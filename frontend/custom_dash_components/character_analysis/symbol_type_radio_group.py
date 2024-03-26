import dash_mantine_components as dmc


class SymbolTypeRadioGroup(dmc.RadioGroup):
    def __init__(self, component_id: str):
        super().__init__([
            dmc.RadioGroup(
                id=component_id,
                label='Отображать символы',
                children=[
                    dmc.Radio('Все', 'all'),
                    dmc.Radio('Алфавит', 'letters'),
                    dmc.Radio('Цифры', 'numbers'),
                    dmc.Radio('Знаки препинания', 'punctuations'),
                    dmc.Radio('Специальные символы', 'specials'),
                ],
                value='all',
                orientation='vertical'
            )
        ])
