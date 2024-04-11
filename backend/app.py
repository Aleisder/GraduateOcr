import base64
from ast import literal_eval

from flask import request, jsonify
from pdf2image import convert_from_bytes

from backend.config import POPPLER_PATH
from backend.ocr_modules.pytesseract_module import PytesseractModule
from backend.ocr_service import OcrService


from flask import Flask

app = Flask(__name__)

ocr_service = OcrService(PytesseractModule())


@app.route('/recognition', methods=['GET'])
def get_recognition():
    decoded = base64.b64decode(request.data)

    images = convert_from_bytes(
        pdf_file=decoded,
        poppler_path=POPPLER_PATH
    )
    reference, experimental = '', ''

    for image in images:
        ref_page, exp_page = ocr_service.get_recognitions(image, 'jpn')
        reference += ''.join(ref_page)
        experimental += ''.join(exp_page)

    return reference + '|' + experimental


@app.route('/character-analysis')
def get_character_analysis():
    pass


@app.route('/reference', methods=['GET'])
def get_reference_recognition():
    # получение json-объекта из запроса
    request_data: dict = literal_eval(request.get_json())
    # получение строкового представления файла из json-объекта
    file_content: str = request_data['file']
    # получение оригинального текста
    document = ocr_service.get_reference(file_content)
    # возвращает json-объект клиенту
    return jsonify(pages=document)


@app.route('/experimental', methods=['GET'])
def get_experimental_recognition():
    decoded = base64.b64decode(request.data)

    images = convert_from_bytes(
        pdf_file=decoded,
        poppler_path=POPPLER_PATH
    )
    document = []

    for image in images:
        exp_page = ocr_service.get_experimental(image)
        document.append(exp_page)
    return jsonify(pages=document)
