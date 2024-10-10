from typing import Generator

from PIL import Image, ImageDraw

coords_format = tuple[float, float, float, float]
colors_format = tuple[int,int,int] | str
colors_dict: dict[str:tuple] = {
    "red": (255, 0, 0),
    "green": (0, 255, 0)
}

def frames_generator(
        image: Image.Image, 
        coords_list: list[coords_format]
    ) -> Generator[Image.Image, None, None]:
    for coords in coords_list:
        yield image.crop(coords)

def draw_over_img(
    img: Image.Image, 
    coordinates: coords_format | list[coords_format], 
    color_fill: colors_format | list[colors_format],
    transparency:float = 0.6
) -> Image.Image:
    FULLY_TRANSPARENT = (0,)
    OVERLAY_TRANSPARENCY = (int(255*transparency),)

    input_img = img.copy().convert("RGBA")

    if isinstance(color_fill, str):
        color_fill = colors_dict.get(color_fill, (0,0,0))
    if isinstance(color_fill, tuple):
        color_fill = [color_fill]

    if isinstance(coordinates, tuple):
        coordinates = [coordinates]
    
    TEMP_COLOR = (0,0,0)

    overlay = Image.new("RGBA", input_img.size, TEMP_COLOR+FULLY_TRANSPARENT)
    draw = ImageDraw.Draw(overlay)

    for coord, color in zip(coordinates, color_fill):
        if isinstance(color, str):
            color = colors_dict.get(color, (0,0,0))
        draw.rectangle(coord, fill=color+OVERLAY_TRANSPARENCY)

    preprocessed_img = Image.alpha_composite(input_img, overlay).convert("RGB")

    return preprocessed_img