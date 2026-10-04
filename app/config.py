from dataclasses import dataclass

@dataclass
class Settings:
    app_name: str = "JY-AI-IQC-Drawing-OCR"
    output_dir: str = "output"
    ocr_backend: str = "tesseract"
    images_dir: str = "samples"

settings = Settings()
