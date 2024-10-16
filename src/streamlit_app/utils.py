from PIL import Image
from fastapi import HTTPException

def get_img_dims(img: Image.Image):
        width, height = img.size
        return width, height

class ApiResponseHandler:
    def __init__(self) -> None:
        pass

    def status_response(self, status_code):
        match status_code:
            case 200:
                return {
                    "status": "200 OK",
                    "message": "Inference completed successfully. The result is returned."
                }
            case 400:
                raise HTTPException(
                    status_code=400, 
                    detail="Bad Request: The input provided is invalid."
                )
            case 422:
                raise HTTPException(
                    status_code=422, 
                    detail="Unprocessable Entity: The input is syntactically correct but cannot be processed for inference."
                )
            case 500:
                raise HTTPException(
                    status_code=500, 
                    detail="Internal Server Error: An error occurred during inference."
                )
            case 503:
                raise HTTPException(
                    status_code=503, 
                    detail="Service Unavailable: The server is under high load or maintenance."
                )
            case _:
                raise HTTPException(
                    status_code=status_code,
                    detail="Unknown Error: Something went wrong."
                )