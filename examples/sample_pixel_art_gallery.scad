use <..\pixel_art.scad>
include <pix_Gallery.scad>

example = 0;

if (example == 0) {
    translate([0, 0, 0]) PixArt(H=Pix00);
    translate([50, 200, 0]) PixArt(H=PixAlien);
    translate([50, 350, 0]) PixArt(H=PixGhost);
    translate([50, 500, 0]) PixArt(H=PixHeart);
    translate([200, 0, 0]) PixArt(H=PixHello);

} else if(example == 1) {
    PixArt(H=Pix00);
} else if(example == 2) {
    PixArt(H=PixAlien);
} else if(example == 3) {
    PixArt(H=PixHello);
} else if(example == 4) {
    PixArt(H=PixGhost);
} else if(example == 5) {
    PixArt(H=PixHeart);
} else {
    echo("Unknown example");
}

