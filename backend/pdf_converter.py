import os
from PIL import Image

for file in os.listdir("./images"):
    image = Image.open(f"./images/{file}")
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.save(f"./pdfs/{os.path.splitext(file)[0]}.pdf", "PDF", resolution=100.0)