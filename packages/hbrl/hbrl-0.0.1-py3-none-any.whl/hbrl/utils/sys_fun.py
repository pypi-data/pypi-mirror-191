import os
import shutil
import datetime
import cv2
import numpy as np
from PIL import Image


def create_dir(dir_name):
    if os.path.isdir(dir_name):
        return
    dir_parts = dir_name.split("/")
    directory_to_create = ""
    for part in dir_parts:
        directory_to_create += part + "/"
        if not os.path.isdir(directory_to_create):
            try:
                os.mkdir(directory_to_create)
            except FileNotFoundError:
                print("failed to create dir " + str(directory_to_create))
                raise Exception


def empty_dir(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def generate_video(images, output_directory: str, filename, convert_to_bgr=True):
    """
    generate a video from the given list of images, and save them at location output_directory/filename.mp4.
    @param images: List of images as numpy array of pixels. For each image, the expected shape is width * height * 3.
        images[n][-1] is expected to be a list of rgb pixels. But BGR pixels are accepted if convert_to_bgr is set to
        false.
    @param output_directory: A path. A '/' is added at the end if there's none in the given path.
    @param filename: a filename. Should not contain "/" characters or '.' except for the extension. If no '.' is found
        (aka no extension) a ".mp4" is added at the end.
    @param convert_to_bgr: (boolean) If True (default value), the colors are considered as RGB and are converted to BGR
        (which is the default opencv standard, don't ask me why).
    """
    # Convert image colors
    if convert_to_bgr:
        images = [cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR) for img in images]

    if output_directory[-1] != "/":
        output_directory += "/"
    assert output_directory.find(".")

    # Verify filename
    if len(filename) < 4 or filename[-4:] != ".mp4":
        filename += ".mp4"
    assert len(filename.split(".")) == 2

    create_dir(output_directory)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    height, width, channels = images[0].shape
    fps = 30

    out = cv2.VideoWriter(output_directory + filename, fourcc, fps, (width, height))
    for image_data in images:
        image_data = image_data.astype(np.uint8)
        out.write(image_data)
    out.release()


def save_image(image: np.ndarray, directory, file_name):
    if directory[-1] != "/":
        directory += "/"
    image = Image.fromarray(image)
    create_dir(directory)
    if not file_name.endswith(".png"):
        if len(file_name.split(".")) > 1:
            file_name = "".join(file_name.split(".")[:-1])  # Remove the last extension
        assert len(file_name.split(".")) == 1
        file_name += ".png"
    image.save(directory + file_name)


def get_red_green_color(value, hexadecimal=True):
    """
    Return a colour that belongs to a gradiant from red (value=0) to green (value=1).
    @param value: value between 0 and 1 that defines result color.
    @param hexadecimal: THe colour will be return in hexadecimal if true, in a list of RGB int otherwise.
    """
    low_color = [255, 0, 0]
    high_color = [0, 255, 0]
    if hexadecimal:
        result = "#"
    else:
        result = []
    for index, (low, high) in enumerate(zip(low_color, high_color)):
        difference = high - low
        if hexadecimal:
            final_color = hex(int(low + value * difference))[2:]
            result += "0" + final_color if len(final_color) == 1 else final_color
        else:
            final_color = int(low + value * difference)
            result.append(final_color)
    return result
