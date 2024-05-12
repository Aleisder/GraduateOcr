import base64
import io
import os
from ast import literal_eval
from datetime import datetime
from flask import request, jsonify, send_file
from pdf2image import convert_from_bytes
from dotenv import load_dotenv
from backend.ocr_modules.pytesseract_module import PytesseractModule
from backend.ocr_service import OcrService
from backend.repository import MinioRepository
from flask import Flask, abort
from flask.wrappers import Response


# подгружает переменные окружения из файла .env
load_dotenv()

app = Flask(__name__)

ocr_service = OcrService(PytesseractModule())
repository = MinioRepository()


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


@app.route('/experimental/<lang>', methods=['GET'])
def get_experimental_recognition(lang: str):

    if lang not in ['chi_sim', 'jpn']:
        error_response = Response(response='Invalid language argument', status=400)
        abort(error_response)

    decoded = base64.b64decode(request.data)

    images = convert_from_bytes(
        pdf_file=decoded,
        poppler_path=os.getenv('POPPLER_PATH')
    )
    document = []

    for image in images:
        exp_page = ocr_service.get_experimental(image, lang)
        document.append(exp_page)
    return jsonify(pages=document)


# получение URL-адресов страниц документа
@app.route('/pages', methods=['GET'])
def store_images():
    decoded: bytes = base64.b64decode(request.data)

    images = convert_from_bytes(
        pdf_file=decoded,
        poppler_path=os.getenv('POPPLER_PATH')
    )
    # список для хранения URL-адресов изображений
    urls = []

    for image in images:
        buffer = io.BytesIO()
        # сохранение изображения в буфер
        image.save(buffer, format='PNG')
        # создание генерация названия файла в формате "YYYY-mm-dd-HH-MM-SS.png"
        filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f') + '.png'
        # загрузка изображения в MinIO и получение URL-адреса
        url = repository.upload_image(filename, buffer.getvalue())
        urls.append(url)
    # возвращаем клиенту ссылки на изображения в формате JSON
    return jsonify(images=urls)


# получение изображения с сервера
@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    # получение изображения с сервера MinIO
    image: io.BytesIO = repository.get_image(filename)
    # отправка файла клиенту
    return send_file(path_or_file=image, mimetype='image/png')
