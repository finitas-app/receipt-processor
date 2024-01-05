from typing import Annotated
from fastapi import FastAPI, File, HTTPException
import uvicorn
from starlette.responses import JSONResponse

from parser import parse_receipt_to_json
from request_formatter import format_request_to_proper_format

app = FastAPI(debug=True)


@app.post(
    "/api/parse",
    responses={
        200: {"description": "Successful request."},
        400: {"description": "Request is badly formatted."},
        415: {"description": "Request type is not allowed."},
    }
)
async def post_parse(file: Annotated[bytes | None, File()] = None):
    if file is None or len(file) == 0:
        return JSONResponse(
            status_code=400,
            content={"errorCode": 'FILE_NOT_PROVIDED', "errorMessage": ""},
        )

    try:
        image = format_request_to_proper_format(file)
        return {"result": parse_receipt_to_json(image)}
    except HTTPException as ex:
        return JSONResponse(
            status_code=ex.status_code,
            content=ex.detail,
        )


@app.get("/")
async def health():
    return {"description": "Server is up"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8081)
