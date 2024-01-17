from flask import Flask, request, render_template
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            return "No file part"

        extracted_text = ""

        if file.filename.endswith(".pdf"):
            images = convert_from_bytes(file.read())
            for image in images:
                extracted_text += pytesseract.image_to_string(image, lang="ara+eng")

        elif file.filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
        ):
            image = Image.open(io.BytesIO(file.read()))
            extracted_text = pytesseract.image_to_string(image, lang="ara+eng")

        else:
            return "Unsupported file format"

        return extracted_text

    return render_template("upload.html")


if __name__ == "__main__":
    app.run()
