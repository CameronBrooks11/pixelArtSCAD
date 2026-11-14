// Hand-written patterns: each is a list of strings, one character per pixel.
// The arrays are in examples/art/pix_Gallery.scad and pix00.scad.
use <../pixel_art.scad>
include <../pix00.scad>
include <art/pix_Gallery.scad>

// Which pattern to draw
example = "all"; // [all, 00, alien, hello, ghost, heart]

if (example == "all") {
    PixArt(H=PixHello);
    translate([0, 120, 0]) PixArt(H=Pix00);
    translate([190, 120, 0]) PixArt(H=PixAlien);
    translate([330, 120, 0]) PixArt(H=PixGhost);
    translate([460, 120, 0]) PixArt(H=PixHeart);
} else if (example == "00") {
    PixArt(H=Pix00);
} else if (example == "alien") {
    PixArt(H=PixAlien);
} else if (example == "hello") {
    PixArt(H=PixHello);
} else if (example == "ghost") {
    PixArt(H=PixGhost);
} else if (example == "heart") {
    PixArt(H=PixHeart);
} else {
    assert(false, str("unknown example ", example));
}
