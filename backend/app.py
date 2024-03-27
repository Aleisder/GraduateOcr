import base64

from flask import Flask, request
from pdf2image import convert_from_bytes

from backend.config import POPPLER_PATH
from backend.ocr_modules.pytesseract_module import PytesseractModule
from backend.ocr_service import OcrService

ocr_service = OcrService(
    reference=PytesseractModule(),
    experimental=PytesseractModule()
)

app = Flask(__name__)
PDF = 'application/pdf'


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

    return reference + '|' + experimental


@app.route('/character-analysis')
def get_character_analysis():
    pass
