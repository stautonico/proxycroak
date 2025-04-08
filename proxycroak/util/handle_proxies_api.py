import io
from base64 import b64encode
from PIL import Image

from flask import render_template, make_response, jsonify
from flask_weasyprint import HTML, CSS
from weasyprint import default_url_fetcher
from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from proxycroak.util.decklist import parse_decklist
from proxycroak.blueprints.ui_api.handle_pic_mode import handle_pic_mode
from proxycroak.blueprints.ui_api.handle_text_mode import handle_text_mode
from proxycroak.logging import logger


def handle_proxies_api(data, opts=None):
    # TODO: There is alot of duplicate code here with `handle_proxies_page`. This should be fixed
    # (make dupe stuff into a function)
    options = opts or {
        "lowres": False,
        "watermark": False,
        "legacy": False,
        "illustration": False,
        "nomin": False,
        "jp": False,
        "exclude_secrets": False
    }

    dl = data["decklist"].replace("\r", "")

    # Remove empty lines
    lines = dl.split("\n")

    while "" in lines:
        lines.remove("")

    if len(lines) > 100:
        logger.error(f"User provided decklist with length {len(lines)}", "decklist::api")
        return [f"decklist too long! (max lines: 100, you provided {len(lines):,})"]

    parsed_list = parse_decklist(data["decklist"])
    if parsed_list is [] or parsed_list is None:
        return ["invalid decklist"]

    # Total up the requested cards. If its > 100, fail
    total = 0
    for i in parsed_list:
        if "amnt" in i:
            total += i["amnt"]

    if total > 100:
        logger.error(f"User requested {total} cards", "decklist::api")
        return [f"decklist too long! (max cards: 100, you provided {total:,})"]

    if data["mode"] == "pic":
        output, errors = handle_pic_mode(parsed_list, options)
    else:
        output, errors = handle_text_mode(parsed_list, options)

    # TODO: Save the decklist?

    html = render_template(
        "pages/proxies.html",
        meta={
            "title": "Proxies",
            "description": "A simple tool for deck testing: choose the format (pics or text), and print up to 3 decks made of combined Pokémon proxy cards.",
            "tags": ["proxies"]
        },
        rows=output,
        errors=errors,
        share_id="TODO",
        options=options)

    def url_fetcher(url):
        if url.startswith("file://"):
            try:
                filepath = url.replace("file://", "")
                f = open(f"proxycroak/{filepath}")
                return {"string": f}
            except Exception as e:
                return default_url_fetcher(url)
        return default_url_fetcher(url)

    with open("proxycroak/static/css/index.css", "r") as f:
        css = CSS(file_obj=f)

    pdf_bytes = HTML(string=html, media_type="print", url_fetcher=url_fetcher).write_pdf(stylesheets=[css])

    try:
        images = convert_from_bytes(pdf_bytes)
    except PDFInfoNotInstalledError:
        print("Poppler not installed TODO: RETURN ERROR AND LOG")
        return "fail"
    except PDFPageCountError:
        print("Something wrong with page count TODO: RETURN ERROR AND LOG")
        return "fail"
    except PDFSyntaxError:
        print("Invalid pdf TODO: RETURN ERROR AND LOG")
        return "fail"
    except Exception as e:
        print(f"Some other shit {e}")
        return "fail"

    def concatenate_images_vertically(image_list):
        # Calculate the total height and the maximum width of the new image
        total_height = sum(img.height for img in image_list)
        max_width = max(img.width for img in image_list)

        # Create a new blank image with the calculated width and height
        concatenated_image = Image.new('RGB', (max_width, total_height))

        # Initialize the y offset to paste each image
        y_offset = 0

        for img in image_list:
            # Paste the image at the current y offset
            concatenated_image.paste(img, (0, y_offset))
            # Update the y offset
            y_offset += img.height

        return concatenated_image

    tallimg = concatenate_images_vertically(images)

    img_bytearray = io.BytesIO()

    tallimg.save(img_bytearray, format="JPEG")
    img_bytearray.seek(0)

    resp = make_response(img_bytearray)
    resp.headers.set("Content-Type", "image/jpeg")
    resp.headers.set(
        'Content-Disposition', 'attachment', filename="proxies.jpeg")


    resp = make_response(pdf_bytes)
    resp.headers.set("Content-Type", "application/pdf")
    resp.headers.set(
        'Content-Disposition', 'attachment', filename="proxies.pdf")

    return jsonify({"errors": "", "pdf": b64encode(pdf_bytes).decode()})
