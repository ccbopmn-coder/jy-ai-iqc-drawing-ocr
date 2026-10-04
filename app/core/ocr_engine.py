import io
import re
from PIL import Image
import pytesseract


def extract_text_from_image(image_bytes: bytes, lang: str = "eng"):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as exc:
        return f"OCR_ERROR: {str(exc)}"
