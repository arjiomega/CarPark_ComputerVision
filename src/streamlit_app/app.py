import requests

import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

from utils.img_preprocess import draw_over_img


class StreamlitApp:
    def __init__(self) -> None:
        self.stroke_width = 1
        self.realtime_update = True
        self.target_image: Image.Image = None

        st.title("Parking Lot Availability Counter")

    def run(self):
        self.sidebar()

        if self.target_image:
            self.interactive_canvas()

            if self.canvas_result.json_data["objects"]:
                self.reports()
                self.predict_view()

    def sidebar(self):
        # TODO: implement polygon
        st.sidebar.title("Settings")
        self.drawing_mode = st.sidebar.selectbox(
            label="Drawing tool:", options=("rectangle")  # , "polygon")
        )

        uploaded_img = st.sidebar.file_uploader("Target image:", type=["png", "jpg"])

        if uploaded_img is not None:
            self.target_image = Image.open(uploaded_img)

    def _get_img_dims(self, img: Image.Image):
        width, height = img.size
        return width, height

    def interactive_canvas(self):
        FILL_COLOR = "rgba(255, 165, 0, 0.3)"
        width, height = self._get_img_dims(self.target_image)

        self.canvas_result = st_canvas(
            fill_color=FILL_COLOR,
            stroke_width=self.stroke_width,
            background_image=self.target_image,
            update_streamlit=self.realtime_update,
            width=width,
            height=height,
            drawing_mode=(
                "rect" if self.drawing_mode == "rectangle" else self.drawing_mode
            ),
            point_display_radius=0,
            display_toolbar=True,
            key="interactive_canvas",
        )

    def reports(self, debug: bool = False):
        import pandas as pd

        self.label_df = pd.json_normalize(self.canvas_result.json_data["objects"])

        if set(["left", "top", "width", "height"]).issubset(self.label_df.columns):
            self.label_df = self.label_df.astype(
                {"left": float, "top": float, "width": float, "height": float}
            )

        if debug:
            st.write(self.label_df)

    def _predict_by_pixel_count(
        self, image, coords_list
    ) -> dict[str, dict[str, list | bool]]:

        inference_type = "by_pixel"
        url = f"http://localhost:8000/api/inference/{inference_type}"

        response = requests.post(
            url,
            json={"image_input": np.array(image).tolist(), "coords_list": coords_list},
        )
        response_data = response.json()

        return response_data

    def _predict_ml(self):
        url = f"http://localhost:8000/api/inference/{inference_type}"

    def inference(self, image, coords_list):
        return self._predict_by_pixel_count(image, coords_list)

    def predict_view(self):

        coords_list = [
            [
                coords_info["left"],  # x1
                coords_info["top"],  # y1
                coords_info["left"] + coords_info["width"],  # x2
                coords_info["top"] + coords_info["height"],  # y2
            ]
            for _, coords_info in self.label_df.iterrows()
        ]

        coords_label_dict = self.inference(self.target_image, coords_list)

        colors_list = [
            "red" if info["label"] == True else "green"
            for info in coords_label_dict.values()
        ]

        processed_img = draw_over_img(self.target_image, coords_list, colors_list)

        st.image(processed_img)


if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
