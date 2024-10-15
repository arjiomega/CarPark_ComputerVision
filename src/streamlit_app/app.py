from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

from streamlit_app.inference import Inference
from shared_utils.img_preprocess import DrawOverImg
from streamlit_app.utils import ApiResponseHandler, get_img_dims

inference_format = dict[str, dict[str, list | bool]]

class StreamlitApp:
    def __init__(
            self, 
            inference_url = "http://localhost:8000/api/inference",
            api_response_handler = ApiResponseHandler
        ) -> None:
        self.stroke_width = 1
        self.realtime_update = True
        self.target_image: Image.Image = None
        self.inference_url = inference_url
        self.inference = Inference(inference_url, api_response_handler).inference
        self.clicked_inference = False
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

    def interactive_canvas(self):
        FILL_COLOR = "rgba(255, 165, 0, 0.3)"
        width, height = get_img_dims(self.target_image)

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

        self.clicked_inference = st.button("run inference")

    def reports(self, debug: bool = False):
        import pandas as pd

        self.label_df = pd.json_normalize(self.canvas_result.json_data["objects"])

        if set(["left", "top", "width", "height"]).issubset(self.label_df.columns):
            self.label_df = self.label_df.astype(
                {"left": float, "top": float, "width": float, "height": float}
            )

        if debug:
            st.write(self.label_df)

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

        result = self.inference(self.target_image, coords_list, inference_type='ml')

        parking_lot_info = result['parking_lot_info']
        cars_info = result['cars_info']

        car_centroids_list = [
            tuple(car['center_point'])
            for car in cars_info.values()
        ]

        colors_list = [
            "red" if info["is_occupied"] == True else "green"
            for info in parking_lot_info.values()
        ]

        text_list = [
            str(space_idx)
            for space_idx in parking_lot_info.keys()
        ]

        draw = DrawOverImg(self.target_image)
        draw.draw_spaces(coords_list, colors_list, text_list)
        draw.draw_car_center_points(car_centroids_list)
        processed_img = draw.get_processed_image()

        st.image(processed_img)


if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
