import dash_mantine_components as dmc


class SelectOcrModule(dmc.MultiSelect):
    def __init__(self, component_id: str):
        super().__init__([
            dmc.MultiSelect(
                id=component_id,
                label='Выберите OCR-инструменты',
                data=[
                    {'value': 'tesseract', 'label': 'Tesseract'},
                    {'value': 'keras', 'label': 'Keras'},
                    {'value': 'pyocr', 'label': 'PyOCR'},
                ],
                value=['tesseract']
            )
        ])
