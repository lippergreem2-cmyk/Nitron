"""
Nitron Image Learning

Receives user-provided images, validates them,
analyzes them, and stores them in Nitron's learning memory.
"""

import base64
import io
import os
import uuid
from datetime import datetime

from brain.learner import learner
from ai.image_analyzer import analyze_image

try:
    from PIL import Image
except ImportError:
    Image = None


IMAGE_DIR = os.path.join(
    os.path.dirname(__file__),
    "brain",
    "learned_images"
)

os.makedirs(IMAGE_DIR, exist_ok=True)


def validate_image(image_data):
    """
    Verify that the supplied bytes contain a valid image.
    """

    if Image is None:
        return

    try:
        with Image.open(io.BytesIO(image_data)) as image:
            image.verify()

    except Exception as e:
        raise ValueError(
            f"Invalid or corrupted image: {e}"
        )


def learn_image(image_base64, filename="image.jpg", note=""):
    """
    Save, analyze, and learn a user-provided image.
    """

    if not image_base64:
        raise ValueError("No image data received.")

    # Remove data-URL prefix if present.
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    try:
        image_data = base64.b64decode(
            image_base64,
            validate=True
        )
    except Exception as e:
        raise ValueError(
            f"Invalid Base64 image data: {e}"
        )

    if not image_data:
        raise ValueError("Decoded image is empty.")

    # Validate BEFORE writing anything to learning memory.
    validate_image(image_data)

    extension = os.path.splitext(filename)[1].lower()

    if extension not in (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    ):
        extension = ".jpg"

    image_id = uuid.uuid4().hex
    saved_name = f"{image_id}{extension}"

    image_path = os.path.join(
        IMAGE_DIR,
        saved_name
    )

    with open(image_path, "wb") as file:
        file.write(image_data)

    topic = f"image_{image_id}"

    # Analyze the validated image.
    try:
        analysis = analyze_image(image_path)

    except Exception as e:
        analysis = {
            "type": "image",
            "path": image_path,
            "filename": filename,
            "analysis": (
                f"Image was saved, but analysis failed: {e}"
            ),
            "text": "",
            "ocr": {
                "success": False,
                "text": "",
                "error": str(e)
            }
        }

    description = analysis.get(
        "analysis",
        "Image received successfully."
    )

    # Add OCR text to the learning description.
    extracted_text = analysis.get(
        "text",
        ""
    ).strip()

    if extracted_text:
        description += (
            "\n\nExtracted text:\n"
            + extracted_text
        )

    if note:
        description += (
            "\n\nUser note: "
            + note
        )

    content = {
        "type": "image",
        "title": filename,
        "image_path": image_path,
        "note": note,
        "description": description,
        "analysis": analysis,
        "text": extracted_text,
        "learned_at": datetime.now().isoformat(),
    }

    entry = learner.learn(
        topic,
        "user_image",
        content
    )

    return {
        "topic": topic,
        "image_path": image_path,
        "analysis": analysis,
        "entry": entry,
    }
