from typing import Annotated

from fastapi import FastAPI, File, HTTPException

from parser import parse_image_to_json
from request_formatter import format_request_to_proper_format

app = FastAPI()


@app.post(
    "/parse",
    responses={
        200: {"description": "Successful request."},
        400: {"description": "Request is badly formatted."},
        415: {"description": "Request type is not allowed."},
    }
)
async def post_parse(file: Annotated[bytes | None, File()] = None):
    if file is None or len(file) == 0:
        raise HTTPException(400, detail="File not provided")

    image = format_request_to_proper_format(file)
    return parse_image_to_json(image)
