import requests
import json


class OcrApi:

    def __init__(self):
        self.BASE_URL = 'http://127.0.0.1:5000'
        self.DEFAULT_HEADERS = {'content_type': 'application/json'}

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

    def experimental_from_file(self, file: str, lang: str) -> list[list[str]]:
        json_data = json.dumps({'file': file})
        r = requests.get(
            url=self.BASE_URL + f'/experimental/{lang}',
            headers=self.DEFAULT_HEADERS,
            json=json_data
        )
        document = []
        for page in r.json()['pages']:
            document.append(page)
        return document

    def get_images_by_document(self, file: str) -> list[str]:
        json_data = json.dumps({'file': file})
        r = requests.get(
            url=self.BASE_URL + '/pages',
            headers=self.DEFAULT_HEADERS,
            json=json_data
        )
        return r.json()
