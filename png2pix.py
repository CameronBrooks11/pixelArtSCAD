"""Convert a PNG image into a character array for pixel_art.scad.

Each pixel becomes the character whose colormap colour is nearest to it.
Fully transparent pixels become a space, which PixArt leaves empty.
"""

import argparse
import re
import sys
from pathlib import Path

from PIL import Image

BLANK = " "
DEFAULT_COLORMAP = Path(__file__).resolve().parent / "colormap.scad"

# One entry of colorMap255, such as ["R", [255, 0, 0]]
ENTRY = re.compile(r'\[\s*"(.)"\s*,\s*\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\s*\]')


def load_colormap(path):
    """Read the character-to-RGB entries of a colormap .scad file, in file order."""
    colormap = {}
    for char, r, g, b in ENTRY.findall(Path(path).read_text(encoding="utf-8")):
        if char == BLANK:
            raise ValueError(f"{path}: the blank character cannot be a colormap entry")
        colormap.setdefault(char, (int(r), int(g), int(b)))
    if not colormap:
        raise ValueError(f"{path}: no colormap entries found")
    return colormap


def closest_color(rgb, colormap):
    """Return the character nearest to rgb; the earlier entry wins a tie."""
    return min(
        colormap,
        key=lambda char: sum((a - b) ** 2 for a, b in zip(rgb, colormap[char], strict=True)),
    )


def image_to_rows(img, colormap, downscale=1):
    """Return one string per image row, top row first."""
    img = img.convert("RGBA")
    if downscale > 1:
        width, height = img.width // downscale, img.height // downscale
        if width < 1 or height < 1:
            raise ValueError(
                f"image is {img.width}x{img.height}, smaller than the downscale factor {downscale}"
            )
        img = img.resize((width, height))
    pixels = img.load()
    cache = {}
    rows = []
    for y in range(img.height):
        row = []
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                row.append(BLANK)
            else:
                rgb = (r, g, b)
                if rgb not in cache:
                    cache[rgb] = closest_color(rgb, colormap)
                row.append(cache[rgb])
        rows.append("".join(row))
    return rows


def format_scad(rows, name):
    lines = [f"{name} = ["]
    lines += [f'\t"{row}",' for row in rows]
    lines.append("];")
    return "\n".join(lines) + "\n"


def default_name(path):
    return "pix_" + re.sub(r"\W", "_", Path(path).stem)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("image", type=Path, help="PNG image to convert")
    parser.add_argument("-o", "--output", type=Path, help="write here instead of stdout")
    parser.add_argument("-n", "--name", help="array name (default: pix_<image name>)")
    parser.add_argument(
        "-d",
        "--downscale",
        type=int,
        default=1,
        metavar="N",
        help="shrink the image by this factor first (default: 1)",
    )
    parser.add_argument(
        "-c",
        "--colormap",
        type=Path,
        default=DEFAULT_COLORMAP,
        help="colormap .scad file (default: the one beside this script)",
    )
    args = parser.parse_args(argv)

    name = args.name or default_name(args.image)
    if not re.fullmatch(r"[A-Za-z_]\w*", name):
        parser.error(f"array name {name!r} is not a valid OpenSCAD identifier")
    if args.downscale < 1:
        parser.error("--downscale must be 1 or more")

    try:
        colormap = load_colormap(args.colormap)
        with Image.open(args.image) as img:
            rows = image_to_rows(img, colormap, args.downscale)
    except (OSError, ValueError) as err:
        print(f"png2pix: {err}", file=sys.stderr)
        return 1

    text = format_scad(rows, name)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
