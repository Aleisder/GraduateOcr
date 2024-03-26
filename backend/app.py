import base64

from pdf2image import convert_from_bytes
from flask import Flask, request
from markupsafe import escape
from backend.config import POPPLER_PATH
from backend.ocr_service import OcrService
from backend.ocr_modules.pytesseract_module import PytesseractModule

ocr_service = OcrService(
    reference=PytesseractModule(),
    experimental=PytesseractModule()
)


app = Flask(__name__)
PDF = 'application/pdf'


@app.route('/')
def hello():
    return '<p>無芸せ波生もへ型近ーは<p>',


@app.route('/recognition')
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

    print(reference, experimental)
    return reference, experimental


@app.route('/character-analysis')
def get_character_analysis():
    pass


@app.route('/path/<path_variable>')
def path_variable_query(path_variable):
    return f'Hello, {escape(path_variable)}'


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return bad_request()
    file = request.files['file']
    if file.content_type != PDF:
        return 'Invalid file format'

    images = convert_from_bytes(
        pdf_file=file.read(),
        poppler_path=POPPLER_PATH
    )
    return f'{len(images)} {images[0].im}'


@app.errorhandler(400)
def bad_request():
    return {
        'code': 400,
        'error': "asdf"
    }
