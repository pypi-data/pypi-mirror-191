import os
import subprocess
from typing import Tuple

from PIL import Image


def crop(
    in_filename: str, bbox: Tuple[int, int, int, int], cleanup: bool = True
) -> str:
    """Crop an image given a filename and a bounding box.

    Args:
        in_filename (str): The filepath of the image to crop.
        bbox (Tuple[int, int, int, int]): (left, upper, right, lower)-tuple.
        cleanup (bool, optional): Whether or not to remove to input filepath. Defaults to True.

    Returns:
        str: The filepath of the cropped image.
    """
    in_file, in_ext = os.path.splitext(in_filename)
    out_file = f"{in_file}-cropped{in_ext}"
    im = Image.open(in_filename)
    im = im.crop(bbox)
    im.save(out_file)
    if cleanup:
        os.remove(in_filename)
    return out_file


def getbbox(in_filename: str) -> Tuple[int, int, int, int]:
    """Get the bounding box of an image file.

    Args:
        in_filename (str): The filepath of the image to get the bounding box for.

    Returns:
        Tuple[int, int, int, int]: The bounding box as a (left, upper, right, lower)-tuple.
    """
    im = Image.open(in_filename)
    return im.getbbox()


def thumbnail(in_filename: str, size: int = 640, cleanup=True) -> str:
    """Generate a thumbnail of an image

    Args:
        in_filename (str): The filepath of the image to generate a thumbnail of.
        size (int, optional): The size of the thumbnail in pixels. Defaults to 640.
        cleanup (bool, optional): Whether or not to remove to input filepath. Defaults to True.

    Returns:
        str: _description_
    """
    in_file, in_ext = os.path.splitext(in_filename)
    out_file = f"{in_file}-thumbnail{in_ext}"
    im = Image.open(in_filename)
    im = im.thumbnail(size)
    im.save(out_file)
    if cleanup:
        os.remove(in_filename)
    return out_file


def convert(in_filename: str, out_filename: str, cleanup=True) -> None:
    """convert a file using `ffmpeg`

    Args:
        in_filename (str): input filepath
        out_filename (str): output filepath including new file extension
        cleanup (bool, optional): whether or not to delete the input filepath. Defaults to True.
    """
    subprocess.check_output(["ffmpeg", "-i", in_filename, out_filename])
    if cleanup:
        os.remove(in_filename)


def cat(in_filename) -> None:
    """
    Prints an image to the console using `imgcat`.

    Args:
        in_filename (str): The filepath of the image to print to the console.
    """
    os.system(f"imgcat {in_filename}")
