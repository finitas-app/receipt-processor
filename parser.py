import logging
import re
import pytesseract
from fastapi import HTTPException

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Daniil\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
logger = logging.getLogger()

product_name_pattern = r'\s*(?P<name>\D+)'
product_price_pattern = r'(?P<price>\d+[,. ]\d+)\D*$'


def parse_receipt_to_json(image):
    try:
        text = pytesseract.image_to_string(image, 'pol')

        logger.info("OCR processing result:")
        logger.info(text)

        return _parse_raw_result_to_json(text)
    except Exception:
        logger.error('Failed to convert request image to a proper format for OCR processing.')
        raise HTTPException(400, detail="Error occurred during receipt processing.")


def _parse_raw_result_to_json(text):
    result = {}

    try:
        for row in text.split("\n"):
            price_match = re.search(product_price_pattern, row)

            if price_match is None:
                continue

            name_match = re.match(product_name_pattern, row)

            if name_match is not None and price_match is not None:
                name = name_match.group('name').strip()
                price = price_match.group('price').strip()
                result[name] = price

        return result
    except Exception:
        logger.error('Failed to parse raw text to JSON format.')
        raise HTTPException(400, detail="Error occurred during receipt processing.")
