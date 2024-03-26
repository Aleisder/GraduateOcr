from base64 import b64decode


def from_str_to_bytes(file: str) -> bytes:
    content_type, content_string = file.split(',')
    return b64decode(content_string)
