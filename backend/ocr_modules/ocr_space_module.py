import requests
from frontend.config import OCR_SPACE_API_KEY

body = {
    'isOverlayRequired': 'false',
    'apikey': OCR_SPACE_API_KEY,
    'language': 'jpn'
}

file = {'file': open(r'C:\Users\danya\Downloads\test1.png', 'rb')}

response = requests.post(
    url='https://api.ocr.space/parse/image',
    files=file,
    data=body
)

print(response.text)


