import os
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from pilkit.processors import ResizeToFill

from config import settings


def resize_image(image):
    img = Image.open(image)
    width, height = img.size[:2]
    baseheight = settings.THUMBNAIL_RESIZE_DIMENSIONS["height"]
    basewidth = settings.THUMBNAIL_RESIZE_DIMENSIONS["width"]
    if width > basewidth or height > baseheight:
        processor = ResizeToFill(200, 200)
        new_img = processor.process(img)
        filename, extension = os.path.splitext(image.name)
        extension = extension.lower()
        if extension == ".png":
            content_type = "image/png"
            img_format = "PNG"
        else:
            content_type = "image/jpeg"
            img_format = "JPEG"
        output = BytesIO()
        if new_img.mode in ("RGBA", "P"):
            new_img = new_img.convert("RGB")
        new_img.save(output, format=img_format, quality=70)
        output.seek(0)
        new_image = InMemoryUploadedFile(
            output,
            "ImageField",
            "%s.%s" % (filename, extension),
            content_type,
            output.__sizeof__(),
            None,
        )
        return new_image
    return image
