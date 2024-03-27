import requests
import json


class OcrApi:

    def __init__(self):
        self.BASE_URL = 'http://127.0.0.1:5000'

    def recognise(self, file_str: str) -> tuple[str, str]:
        data = json.dumps({'file_bytes': file_str})

        r = requests.get(
            url=self.BASE_URL + '/recognition',
            headers={'content_type': 'application/json'},
            data=file_str
        )

        if r.status_code != 200:
            return 'error', 'error'

        ref, exp = r.text.split('|')
        return ref, exp
