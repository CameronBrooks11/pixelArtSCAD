from PIL import Image
import os
import math


def load_colormap(file_path):
    """
    Loads the colormap from a SCAD-like file with RGB values.

    Returns:
        dict: A dictionary where keys are characters and values are RGB tuples.
    """
    colormap = {}
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            # Skip comments, empty lines, and non-data lines
            if line.startswith("//") or not line:
                continue
            if line.startswith("[") and "]," in line:
                try:
                    # Parse entries like ["R", [255, 0, 0]]
                    start = line.find("[")
                    end = line.find("],")
                    char, rgb = line[start + 1 : end].split(", [")
                    char = char.strip('" ')
                    rgb = tuple(map(int, rgb.strip("]").split(",")))
                    colormap[char] = rgb
                    print(f"[DEBUG] Added color: {char} -> {rgb}")
                except ValueError as e:
                    print(f"[WARNING] Skipping invalid line: {line} | Error: {e}")
            else:
                print(f"[INFO] Ignored line: {line}")
    print(f"[DEBUG] Loaded colormap: {colormap.keys()}")
    return colormap


def closest_color(r, g, b, colormap):
    """
    Finds the closest color in the colormap to the given RGB value.
    """
    min_distance = float("inf")
    closest_char = " "
    for char, (cr, cg, cb) in colormap.items():
        distance = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_char = char
    return closest_char


def image_to_pixel_array(
    file_path, resolution=1, colormap_path="colormap.scad", blank_char=" "
):
    """
    Converts a PNG image to a pixel array using a colormap.
    """
    colormap = load_colormap(colormap_path)
    if not colormap:
        raise ValueError("Colormap is empty or invalid!")

    # Load the image
    img = Image.open(file_path).convert("RGBA")  # Ensure RGBA mode
    if resolution > 1:
        img = img.resize((img.width // resolution, img.height // resolution))

    # Get pixel data
    pixels = img.load()
    width, height = img.size
    print(f"[DEBUG] Image size: {width}x{height}, Resolution: {resolution}")

    # Initialize the pixel array
    pixel_array = []
    for y in range(height):
        row = ""
        ignored_count = 0  # Track ignored (transparent) pixels in this row
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:  # Transparent pixel
                row += blank_char
                ignored_count += 1
            else:
                matched_char = closest_color(r, g, b, colormap)
                row += matched_char
        pixel_array.append(row)
        # Summarize the row processing
        print(
            f"[DEBUG] Row {y}: Processed {width - ignored_count} pixels, Ignored {ignored_count}"
        )

    print("[DEBUG] Finished processing image into pixel array.")
    return pixel_array


def save_pixel_array_to_scad(
    pixel_array, output_path, var_name="customPixArray", indent="    ", newline="\n"
):
    """
    Saves the pixel array to a SCAD file with proper OpenSCAD array formatting.
    """
    with open(output_path, "w") as file:
        file.write(f"{var_name} = [{newline}")
        for row in pixel_array:
            file.write(f'{indent}"{row}",{newline}')
        file.write("];")
    print(f"[DEBUG] Pixel array saved to {output_path}")


# Example usage
current_dir = os.getcwd()
resolution = 4  # Adjust resolution
var_name = "PixCustom"  # Custom array name
input_name = "ckbGitHubProfile.png"  # Input image file
output_name = "customPixArrayArray.scad"  # Output SCAD file
colormap_name = "colormap.scad"  # Colormap file

indent = "\t"  # Use tabs for indentation
newline = "\n"  # Newline style for SCAD formatting
file_path = os.path.join(current_dir, input_name)
output_path = os.path.join(current_dir, output_name)
colormap_path = os.path.join(current_dir, colormap_name)

try:
    pixel_array = image_to_pixel_array(
        file_path, resolution, colormap_path=colormap_path
    )
    save_pixel_array_to_scad(
        pixel_array, output_path, var_name=var_name, indent=indent, newline=newline
    )
    print("[INFO] Pixel array processing completed successfully.")
except Exception as e:
    print(f"[ERROR] {e}")
