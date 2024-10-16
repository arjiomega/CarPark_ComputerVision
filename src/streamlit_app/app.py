from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

from streamlit.delta_generator import DeltaGenerator
from shared_utils.img_preprocess import DrawOverImg

try:
    from streamlit_app.inference import Inference
    from streamlit_app.utils import ApiResponseHandler, get_img_dims
except ImportError:
    from inference import Inference # type: ignore
    from utils import ApiResponseHandler, get_img_dims # type: ignore

inference_format = dict[str, dict[str, list | bool]]

class StreamlitApp:
    def __init__(
            self, 
            inference_url = "http://localhost:8000/api/inference",
            api_response_handler = ApiResponseHandler
        ) -> None:
        st.set_page_config(layout="wide")
        self.stroke_width = 1
        self.realtime_update = True
        self.target_image: Image.Image = None
        self.inference_url = inference_url
        self.inference = Inference(inference_url, api_response_handler).inference
        self.clicked_inference = False
        st.title("Parking Lot Availability Counter")

    def _is_canvas_object_available(self):
        """Safely retrieve and return objects from the canvas result."""
        if self.canvas_result.json_data and "objects" in self.canvas_result.json_data:
            objects = self.canvas_result.json_data["objects"]
            return True if objects else False
        return True

    def run(self):
        self.sidebar()
        self.main_app()

    def sidebar(self):
        # TODO: implement polygon
        st.sidebar.title("Settings")
        self.drawing_mode = st.sidebar.selectbox(
            label="Drawing tool:", options=("rectangle")  # , "polygon")
        )

        uploaded_img = st.sidebar.file_uploader("Target image:", type=["png", "jpg"])

        if uploaded_img is not None:
            self.target_image = Image.open(uploaded_img)

    def main_app(self):
        upload_column, inference_column = st.columns(2)

        if self.target_image:
            self.interactive_canvas(upload_column)

            if self._is_canvas_object_available():
                self.reports(upload_column)
                self.predict_view(inference_column)

    def interactive_canvas(self, st_generator_column: DeltaGenerator):
        FILL_COLOR = "rgba(255, 165, 0, 0.3)"
        width, height = get_img_dims(self.target_image)

        with st_generator_column:
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

            left_button, right_button = st.columns([0.3,1], gap='small')

            self.clicked_inference_by_pixel = left_button.button("inference by pixel")
            self.clicked_inference_ml = right_button.button("inference by ml")

    def reports(self, st_generator_column: DeltaGenerator = None, debug: bool = False):
        import pandas as pd

        if self._is_canvas_object_available():
            label_df = pd.json_normalize(self.canvas_result.json_data["objects"])

            if set(["left", "top", "width", "height"]).issubset(label_df.columns):
                label_df = label_df.astype(
                    {"left": float, "top": float, "width": float, "height": float}
                )

            self.coords_list = [
                [
                    coords_info["left"],  # x1
                    coords_info["top"],  # y1
                    coords_info["left"] + coords_info["width"],  # x2
                    coords_info["top"] + coords_info["height"],  # y2
                ]
                for _, coords_info in label_df.iterrows()
            ]

            if debug and st_generator_column:
                st_generator_column.write(label_df)

    def predict_view(self, st_generator_column: DeltaGenerator):

        inference_type = None

        with st_generator_column:
            if self.clicked_inference_by_pixel:
                inference_type = 'by_pixel'
            if self.clicked_inference_ml:
                inference_type = 'ml'

            if inference_type:
                result = self.inference(
                    self.target_image, 
                    self.coords_list, 
                    inference_type=inference_type
                )

                parking_lot_info = result['parking_lot_info']
                cars_info = result['cars_info']

                colors_list = [
                    "red" if info["is_occupied"] == True else "green"
                    for info in parking_lot_info.values()
                ]

                text_list = [
                    str(space_idx)
                    for space_idx in parking_lot_info.keys()
                ]

                draw = DrawOverImg(self.target_image)
                draw.draw_spaces(self.coords_list, colors_list, text_list)

                if cars_info:
                    car_centroids_list = [
                        tuple(car['center_point'])
                        for car in cars_info.values()
                    ]
                    draw.draw_car_center_points(car_centroids_list)

                processed_img = draw.get_processed_image()
                st.image(processed_img)


if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
