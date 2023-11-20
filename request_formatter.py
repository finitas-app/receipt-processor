import io
from logger_instance import logger

import cv2
import numpy as np
from exceptions import UnsupportedMediaTypeException, ErrorCode


def format_request_to_proper_format(request_file):
    try:
        logger.info('Converting image to OCR processing format.')

        image_stream = io.BytesIO(request_file)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)

        return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    except Exception:
        logger.error('Failed to convert request image to a proper format for OCR processing.')
        raise UnsupportedMediaTypeException(
            error_code=ErrorCode.INVALID_FILE_PROVIDED,
            error_message="File invalid. Failed to format.",
        )
