import re
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import png2pix  # noqa: E402

COLORMAP = ROOT / "colormap.scad"


def rows_of(scad_text):
    return re.findall(r'"([^"]*)"', scad_text)


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "png2pix.py"), *map(str, args)],
        capture_output=True,
        text=True,
    )


def test_load_colormap_reads_every_entry_of_the_shipped_map():
    colormap = png2pix.load_colormap(COLORMAP)
    assert colormap["R"] == (255, 0, 0)
    assert colormap["V"] == (120, 81, 169)
    assert list(colormap)[:2] == ["0", "1"]
    assert len(colormap) == 16


def test_load_colormap_ignores_code_and_comments(tmp_path):
    path = tmp_path / "map.scad"
    path.write_text(
        "// a comment\n"
        "colorMap255 = [\n"
        '    ["A", [1, 2, 3]],   // first\n'
        '    ["B",[4,5,6]]\n'
        "];\n"
        "colorMap = [for (entry = colorMap255) [entry[0], normalizeColor(entry[1])]];\n"
    )
    assert png2pix.load_colormap(path) == {"A": (1, 2, 3), "B": (4, 5, 6)}


def test_load_colormap_rejects_a_file_with_no_entries(tmp_path):
    path = tmp_path / "empty.scad"
    path.write_text("// nothing here\n")
    with pytest.raises(ValueError, match="no colormap entries"):
        png2pix.load_colormap(path)


def test_load_colormap_rejects_the_blank_character(tmp_path):
    path = tmp_path / "blank.scad"
    path.write_text('colorMap255 = [[" ", [1, 2, 3]]];\n')
    with pytest.raises(ValueError, match="blank"):
        png2pix.load_colormap(path)


def test_closest_color_picks_the_nearest_and_the_first_of_a_tie():
    colormap = {"0": (0, 0, 0), "B": (0, 0, 0), "W": (255, 255, 255), "R": (255, 0, 0)}
    assert png2pix.closest_color((250, 10, 10), colormap) == "R"
    assert png2pix.closest_color((240, 240, 240), colormap) == "W"
    assert png2pix.closest_color((3, 3, 3), colormap) == "0"


def test_image_rows_run_top_to_bottom_and_transparent_is_blank():
    img = Image.new("RGBA", (3, 2), (0, 0, 0, 0))
    img.putpixel((0, 0), (255, 0, 0, 255))
    img.putpixel((2, 0), (255, 255, 255, 255))
    img.putpixel((1, 1), (0, 0, 0, 255))
    colormap = {"R": (255, 0, 0), "W": (255, 255, 255), "0": (0, 0, 0)}
    assert png2pix.image_to_rows(img, colormap) == ["R W", " 0 "]


def test_downscale_divides_both_dimensions():
    img = Image.new("RGBA", (8, 4), (255, 0, 0, 255))
    rows = png2pix.image_to_rows(img, {"R": (255, 0, 0)}, downscale=4)
    assert rows == ["RR"]


def test_downscale_below_one_pixel_is_an_error():
    img = Image.new("RGBA", (3, 3), (255, 0, 0, 255))
    with pytest.raises(ValueError, match="smaller than"):
        png2pix.image_to_rows(img, {"R": (255, 0, 0)}, downscale=4)


def test_format_scad_is_an_openscad_array():
    assert png2pix.format_scad(["R W", " 0 "], "PixTest") == (
        'PixTest = [\n\t"R W",\n\t" 0 ",\n];\n'
    )


def test_cli_writes_the_array_and_exits_zero(tmp_path):
    png = tmp_path / "dot.png"
    Image.new("RGBA", (2, 1), (255, 0, 0, 255)).save(png)
    out = tmp_path / "dot.scad"
    result = run_cli(png, "-o", out, "--name", "PixDot")
    assert result.returncode == 0, result.stderr
    assert out.read_text() == 'PixDot = [\n\t"RR",\n];\n'
    assert result.stdout == ""


def test_cli_prints_to_stdout_without_an_output_path(tmp_path):
    png = tmp_path / "my-dot.png"
    Image.new("RGBA", (1, 1), (0, 255, 0, 255)).save(png)
    result = run_cli(png)
    assert result.returncode == 0, result.stderr
    assert result.stdout == 'pix_my_dot = [\n\t"G",\n];\n'


def test_cli_missing_input_exits_nonzero_with_a_message(tmp_path):
    result = run_cli(tmp_path / "nope.png")
    assert result.returncode != 0
    assert "nope.png" in result.stderr


def test_cli_rejects_a_name_that_is_not_an_identifier(tmp_path):
    png = tmp_path / "dot.png"
    Image.new("RGBA", (1, 1), (255, 0, 0, 255)).save(png)
    result = run_cli(png, "--name", "not valid")
    assert result.returncode != 0
    assert "not valid" in result.stderr


def test_committed_example_is_what_the_converter_produces():
    result = run_cli(ROOT / "examples" / "art" / "ckbGitHubProfile.png", "--downscale", "4")
    assert result.returncode == 0, result.stderr
    committed = (ROOT / "examples" / "art" / "pix_ckbGH.scad").read_text()
    assert rows_of(result.stdout) == rows_of(committed)
