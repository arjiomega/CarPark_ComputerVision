import cv2
import numpy as np
from utils.img_preprocess import frames_generator


def count_lot_pixel(lot_frame, _debug: bool = False) -> dict[str, int | np.ndarray]:
    """
    Process an image frame to count the number of non-zero pixels in a parking lot area.

    This function converts the input image to grayscale, applies Gaussian blur,
    adaptive thresholding, and median blur to isolate the relevant features.
    Finally, it dilates the image and counts the number of non-zero (white) pixels,
    which represent areas of interest (e.g., occupied parking spaces).

    Args:
        lot_frame (numpy.ndarray): The input image frame in BGR format representing the parking lot.

    Returns:
        dict: A dictionary with the non-zero pixel count and optionally the processed image frame.

    Raises:
        cv2.error: If there is an issue during image processing (e.g., incorrect format).
    """
    input_frame = np.array(lot_frame)
    input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)

    ksize = 3
    imgBlur_ksize = (ksize, ksize)
    imgBlur_sigmaX = 1
    input_frame = cv2.GaussianBlur(input_frame, imgBlur_ksize, imgBlur_sigmaX)

    block_size = 25
    constant = 16
    input_frame = cv2.adaptiveThreshold(
        input_frame,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        block_size,
        constant,
    )

    kernel_size = 5
    input_frame = cv2.medianBlur(input_frame, kernel_size)

    kernel = np.ones((3, 3), np.uint8)
    input_frame = cv2.dilate(input_frame, kernel, iterations=1)

    result = {"non_zero_pixel_count": cv2.countNonZero(input_frame)}

    if _debug:
        result["processed_frame"] = input_frame

    return result


def predict_by_pixel_count(image_frame, coords_list) -> list[bool]:
    PIXEL_COUNT_FOR_OCCUPIED = 300
    return [
        count_lot_pixel(frame)["non_zero_pixel_count"] > PIXEL_COUNT_FOR_OCCUPIED
        for frame in frames_generator(image_frame, coords_list)
    ]

#################################
#               TEST
#################################
def test_count_lot_pixel(image_path):
    """
    Test the count_lot_pixel function with a given image path.

    Args:
        image_path (str): The file path to the image used for testing.

    Displays:
        The original and processed images side by side using cv2.imshow.
    """
    # Load the image
    original_frame = cv2.imread(image_path)

    # Check if the image is loaded properly
    if original_frame is None:
        print("Error: Could not load the image.")
        return

    print(original_frame)

    # Process the image and count non-zero pixels
    result_dict = count_lot_pixel(original_frame, _debug=True)

    cv2.imshow("test", original_frame)

    count, processed_frame = (
        result_dict["non_zero_pixel_count"],
        result_dict["processed_frame"],
    )

    # Display the results
    print(f"Non-zero pixel count: {count}")

    print(processed_frame.shape)

    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2RGB)

    # Stack original and processed images horizontally for comparison
    combined_image = np.hstack((original_frame, processed_frame))

    # Display images
    cv2.imshow("Original vs Processed", combined_image)

    # Wait for a key press and close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()