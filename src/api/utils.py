from api.predict.vanilla import count_lot_pixel
from utils.img_preprocess import frames_generator

def predict_by_pixel_count(image_frame, coords_list) -> list[bool]:
        PIXEL_COUNT_FOR_OCCUPIED = 300
        return [
            count_lot_pixel(frame)["non_zero_pixel_count"] > PIXEL_COUNT_FOR_OCCUPIED
            for frame in frames_generator(image_frame, coords_list)
        ]

