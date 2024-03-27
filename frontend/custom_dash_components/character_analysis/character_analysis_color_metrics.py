import dash_mantine_components as dmc
from frontend import custom_dash_components as cdc


class CharacterAnalysisColorMetrics(dmc.Paper):
    def __init__(self):
        super().__init__([
            cdc.ColorMetrics(
                metrics=[
                    {'color': '#59FF85', 'metric': 'все символы распознаны верно (100%)'},
                    {'color': '#A6FFBD', 'metric': 'есть недочёты (90-100%)'},
                    {'color': '#FFFC66', 'metric': 'встречаются ошибки (70-90%)'},
                    {'color': '#FF6D45', 'metric': 'присутствует много несовпадений (<70%)'},
                ]
            )
        ])
