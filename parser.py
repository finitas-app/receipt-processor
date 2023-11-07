import logging
import re

import pytesseract
from fastapi import HTTPException

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Daniil\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

total_pattern = r'suma'
product_name_pattern = r'\s*(?P<name>\D+)'
product_price_pattern = r'(?P<price>\d+[,. ]\d+)\D*$'


def parse_image_to_json(image):
    try:
        text = pytesseract.image_to_string(image, 'pol')

        logging.info("OCR processing result:")
        logging.info(text)

        return _parse_raw_result_to_json(text)
    except Exception:
        logging.error('Failed to convert request image to a proper format for OCR processing.')
        raise HTTPException(400, detail="Error occurred during receipt processing.")


def _parse_raw_result_to_json(text):
    try:
        result = {}

        items_started = False
        for row in text.split("\n"):
            if items_started is True and re.search(product_price_pattern, row) is None:
                break

            if re.search(product_price_pattern, row) is None:
                continue

            items_started = True
            name_match = re.match(product_name_pattern, row)
            price_match = re.search(product_price_pattern, row)

            if name_match is not None and price_match is not None:
                name = name_match.group('name').strip()
                price = price_match.group('price').strip()
                result[name] = price

        return result
    except Exception:
        logging.error('Failed to parse raw text to JSON format.')
        raise HTTPException(400, detail="Error occurred during receipt processing.")
