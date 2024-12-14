use <..\pixel_art.scad>
include <pix_Gallery.scad>

example = 0;

if(example == 0) {
    PixArt(H=Pix00);
} else if(example == 1) {
    PixArt(H=PixAlien);
} else if(example == 2) {
    PixArt(H=PixHello);
} else if(example == 3) {
    PixArt(H=PixGhost);
} else if(example == 4) {
    PixArt(H=PixHeart);
} else {
    echo("Unknown example");
}