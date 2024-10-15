from typing import Generator

from PIL import Image, ImageDraw

coords_format = tuple[float, float, float, float]
colors_format = tuple[int, int, int] | str
colors_dict: dict[str:tuple] = {"red": (255, 0, 0), "green": (0, 255, 0)}

def get_centroid(coords: coords_format) -> tuple[int, int]:
    x1, y1, x2, y2 = coords
    centroid_x, centroid_y = x1+((x2-x1) / 2), y1+((y2-y1) / 2)
    return (int(centroid_x),int(centroid_y))

def is_inside_boundary(boundary: coords_format, center_point: tuple[float, float]) -> bool:
    x1, y1, x2, y2 = boundary
    center_x, center_y = center_point

    return (x2 >= center_x >= x1) and (y2 >= center_y >= y1)


def frames_generator(
    image: Image.Image, coords_list: list[coords_format]
) -> Generator[Image.Image, None, None]:
    for coords in coords_list:
        yield image.crop(coords)

from PIL import Image, ImageDraw, ImageFont
from shared_utils.img_preprocess import get_centroid

class DrawOverImg:
    FULLY_TRANSPARENT = (0,)
    def __init__(
            self,
            img: Image.Image,
            transparency: float = 0.6
        ) -> None:
        
        self.OVERLAY_TRANSPARENCY = (int(255 * transparency),)
        self.input_img = img.copy().convert("RGBA")

        TEMP_COLOR = (0, 0, 0)
        self.overlay = Image.new("RGBA", self.input_img.size, TEMP_COLOR + self.FULLY_TRANSPARENT)
        self.draw = ImageDraw.Draw(self.overlay)

    def draw_car_center_points(self, car_center_points: list[tuple[int,int]]):
        for car in car_center_points:
            self.draw.circle(car, radius=2, fill=(0, 0, 0), width=3)

    def _write_text(
            self, 
            text, 
            coords, 
            font_size: int = 20, 
            text_color: tuple[int, int, int] = (255, 255, 255)
        ):
        centroid_x, centroid_y = get_centroid(coords)

        # Load a font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Draw the text at the centroid of the rectangle
        text_width, text_height = self.draw.textbbox((10, 10), text, font=font)[2:]  # Use textbbox to get dimensions
        text_position = (centroid_x - text_width / 2, centroid_y - text_height / 2)
        self.draw.text(text_position, text, fill=text_color, font=font)

    def _draw_space(self, space_coords: coords_format):
        pass

    def draw_spaces(
            self, 
            lot_coords: list[coords_format], 
            color_fill_list: list[colors_format],
            text_list: list[str] = None
        ):
        if not text_list:
            text_list = [None]*len(lot_coords)
        for coords, color, text in zip(lot_coords, color_fill_list, text_list):
            if isinstance(color, str):
                color = colors_dict.get(color, (0, 0, 0))
            self.draw.rectangle(coords, fill=color + self.OVERLAY_TRANSPARENCY)
            if text:
                self._write_text(text, coords)

    def get_processed_image(self):
        return Image.alpha_composite(self.input_img, self.overlay).convert("RGB")