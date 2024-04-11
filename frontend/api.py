import requests
import json


class OcrApi:

    def __init__(self):
        self.BASE_URL = 'http://127.0.0.1:5000'
        self.DEFAULT_HEADERS = {'content_type': 'application/json'}

    def recognise(self, file_str: str) -> tuple[str, str]:
        data = json.dumps({'file_bytes': file_str})

        r = requests.get(
            url=self.BASE_URL + '/recognition',
            headers=self.DEFAULT_HEADERS,
            data=file_str
        )

        if r.status_code != 200:
            return 'error', 'error'

        ref, exp = r.text.split('|')
        return ref, exp

    def reference_from_file(self, file: str) -> list[list[str]]:
        json_data = json.dumps({'file': file})
        r = requests.get(
            url=self.BASE_URL + '/reference',
            headers=self.DEFAULT_HEADERS,
            json=json_data
        )
        document = []
        for page in r.json()['pages']:
            document.append(page)
        return document

    def experimental_from_file(self, file: str) -> list[list[str]]:
        json_data = json.dumps({'file': file})
        r = requests.get(
            url=self.BASE_URL + '/experimental',
            headers=self.DEFAULT_HEADERS,
            json=json_data
        )
        document = []
        for page in r.json()['pages']:
            document.append(page)
        return document
