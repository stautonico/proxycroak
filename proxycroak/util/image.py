from PIL import Image
import io


def convert_to_webp(image_content, save_location):
    im = Image.open(io.BytesIO(image_content))

    im.save(save_location, format="webp")
