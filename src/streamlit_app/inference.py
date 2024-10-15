from typing import Literal
import requests

import numpy as np

from streamlit_app.utils import ApiResponseHandler

inference_format = dict[str, dict[str, list | bool]]


class Inference:
    def __init__(
            self, 
            url = "http://localhost:8000/api/inference", 
            api_response_handler = ApiResponseHandler
        ) -> None:
        self.url = url
        self.api_response_handler = api_response_handler()

    def _inference_request(self, url, image_list, coords_list) -> inference_format:
        response = requests.post(
            url,
            json={"image_input": image_list, "coords_list": coords_list},
        )
        response_dict = self.api_response_handler.status_response(response.status_code)
        if response.status_code == 200:
            response_dict["api_output"] = response.json()
            # st.write("api response: ")
            response_data = response.json()

            return response_data

    def _predict_by_pixel_count(
        self, image, coords_list
    ) -> dict[str, dict[str, list | bool]]:

        inference_type = "by_pixel"
        url = f"{self.url}/{inference_type}"

        return self._inference_request(url, np.array(image).tolist(), coords_list)
    
    def _predict_ml(self, image, coords_list, model_name: str = "yolo") -> inference_format:
        inference_type = "ml"
        url = f"{self.url}/{inference_type}/{model_name}"

        return self._inference_request(url, np.array(image).tolist(), coords_list)
    
    def inference(self, image, coords_list, inference_type: Literal["by_pixel", "ml"]) -> inference_format:
        if inference_type == "by_pixel":
            return self._predict_by_pixel_count(image, coords_list)
        if inference_type == "ml":
            model_name = "yolo"
            return self._predict_ml(image, coords_list, model_name)