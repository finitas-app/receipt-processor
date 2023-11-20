from typing import Annotated

import uvicorn
from fastapi import FastAPI, File
from fastapi.responses import JSONResponse

from exceptions import BadRequestException, ProjectBaseException
from exceptions import ErrorCode
from parser import parse_receipt_to_json
from request_formatter import format_request_to_proper_format

app = FastAPI(debug=True)


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
        raise BadRequestException(
            error_code=ErrorCode.FILE_NOT_PROVIDED,
        )

    image = format_request_to_proper_format(file)
    return {"result": parse_receipt_to_json(image)}


@app.get("/")
async def health():
    return {"description": "Server is up"}


@app.exception_handler(ProjectBaseException)
async def unicorn_exception_handler(_, exc: ProjectBaseException):
    return JSONResponse(
        status_code=exc.http_status_code,
        content={
            "errorCode": exc.error_code.value,
            "errorMessage": exc.error_message,
        },
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8081)
