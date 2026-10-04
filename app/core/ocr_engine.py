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


def extract_title_block_fields(text: str):
    field_map = {
        "drawing_no": None,
        "part_name": None,
        "material": None,
        "heat_treatment": None,
        "scale": None,
    }

    patterns = {
        "drawing_no": [r"DRAWING\s*NO\.?\s*[:#-]?\s*([A-Za-z0-9\-]+)", r"图号\s*[:：]?\s*([A-Za-z0-9\-]+)"],
        "part_name": [r"PART\s*NAME\s*[:#-]?\s*([A-Za-z0-9\s\-]+)", r"零件名称\s*[:：]?\s*([A-Za-z0-9\s\-]+)"],
        "material": [r"MATERIAL\s*[:#-]?\s*([A-Za-z0-9\s\-]+)", r"材料\s*[:：]?\s*([A-Za-z0-9\s\-]+)"],
        "heat_treatment": [r"HEAT\s*TREATMENT\s*[:#-]?\s*([A-Za-z0-9\s\-]+)", r"热处理\s*[:：]?\s*([A-Za-z0-9\s\-]+)"],
        "scale": [r"SCALE\s*[:#-]?\s*([A-Za-z0-9\./\-]+)", r"比例\s*[:：]?\s*([A-Za-z0-9\./\-]+)"],
    }

    for key, regexes in patterns.items():
        for pattern in regexes:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                field_map[key] = match.group(1).strip()
                break

    return field_map


def extract_dimension_items(text: str):
    patterns = [
        r"Ø\s*\d+(?:\.\d+)?",
        r"R\s*\d+(?:\.\d+)?",
        r"\d+(?:\.\d+)?\s*±\s*\d+(?:\.\d+)?",
        r"\d+(?:\.\d+)?\s*°",
        r"Ra\s*\d+(?:\.\d+)?",
        r"\d+(?:\.\d+)?\s*mm",
        r"\d+(?:\.\d+)?\s*in",
        r"\d+(?:\.\d+)?\s*μm",
    ]
    matches = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value = match.group(0).strip()
            if value not in matches:
                matches.append(value)
    return matches


def normalize_text(text: str):
    return re.sub(r"\s+", " ", text)
