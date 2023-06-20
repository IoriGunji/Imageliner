import os
import re
import glob
from typing import Final, List
from PIL import Image
import webcolors


COLOR: Final[str] = '#000000'
BORDER_SIZE: Final[str] = 1
IMAGE_EXTS: Final[List[str]] = ['png', 'jpg', 'bmp']


def main():
    chdir = os.path.dirname(__file__)
    files = glob.glob(os.path.join(chdir, '*'))
    for file in files:
        for ext in IMAGE_EXTS:
            if re.search(f'\.{ext}$', file):
                image_edit(file, BORDER_SIZE, COLOR)


def image_edit(img_path: str, border: str, color: str):
    img = Image.open(img_path)
    dir, file = os.path.split(img_path)
    output = 'resized'
    os.makedirs(os.path.join(dir, output), exist_ok=True)
    new_img = add_border(img, border, color)
    new_img.save(os.path.join(dir, output, file), quality = 100)


def add_border(pil_img: Image, border: str, color: str):
    return campus_resize(pil_img, border, border, border, border, color)


def campus_resize(pil_img: Image, top: int, right: int, bottom: int, left: int, color: str):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    rgb = webcolors.hex_to_rgb(color)
    new_pil_img = Image.new(pil_img.mode, (new_width, new_height), rgb)
    new_pil_img.paste(pil_img, (left, top))
    return new_pil_img


if __name__ == "__main__":
    main()
