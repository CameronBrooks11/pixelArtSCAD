use <../pixel_art.scad>
include <../pix00.scad>
include <pix_Gallery.scad>

example = 0;

if (example == 0) {
    PixArt(H=PixHello);
    translate([0, 120, 0]) PixArt(H=Pix00);
    translate([190, 120, 0]) PixArt(H=PixAlien);
    translate([330, 120, 0]) PixArt(H=PixGhost);
    translate([460, 120, 0]) PixArt(H=PixHeart);

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
