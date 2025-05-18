import base64
import io
from typing import List, Union

import pdf2image
from pdf2image import convert_from_bytes
from PIL import Image


def get_images_from_pdf(pdf_bytes: bytes) -> Union[List[Image.Image], None]:
    try:
        return convert_from_bytes(
            pdf_bytes, poppler_path=None, grayscale=False, dpi=300
        )
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        return None


# Helper function to convert image to base64
def image_to_base64(image: Image.Image, format="PNG") -> str:
    """Converts a PIL Image to a Base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
