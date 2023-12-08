from PIL import Image
import io


def convert_to_webp(image_content, save_location):
    im = Image.open(io.BytesIO(image_content))

    im.save(save_location, format="webp")


def make_cropped_image(image_content, save_location, area):
    im = Image.open(io.BytesIO(image_content))

    cropped = im.crop(area)

    cropped.save(save_location, format="webp")
