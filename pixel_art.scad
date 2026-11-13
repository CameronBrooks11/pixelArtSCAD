// pixel_art.scad
include <colormap.scad> // Include the color map
include <pix00.scad>    // Import the default pixel art

Epsilon = 1 / 10000; // Small overlap so neighbouring pixels fuse into one solid

//------------------------------------------------------------
// PixArt
//
// H      list of strings, one per row, top row first. A space leaves the
//        pixel empty; any other character is looked up in the color map.
// pixel  side length of one pixel, in millimetres
// height pixel height, in millimetres
//
// The art lies in the XY plane and reads upright from above: the first
// character of the last row sits at the origin.
//------------------------------------------------------------
module PixArt(H = Pix00, pixel = 10, height = 10)
{
    rows = len(H);
    for (i = [0:rows - 1], j = [0:len(H[i]) - 1])
    {
        if (H[i][j] != " ")
        {
            color(getColor(H[i][j])) translate([ j * pixel, (rows - 1 - i) * pixel, 0 ]) Pixel(pixel, height);
        }
    }
}

// Function to get color based on character using external map
function getColor(char) = let(index = searchIndex(char))(index == -1) ? "gold" : colorMap[index][1];

// Helper function to find the index of a character in the color map
function searchIndex(char, i = 0) = (i == len(colorMap)) ? -1 : (colorMap[i][0] == char) ? i : searchIndex(char, i + 1);

// The Pixel
module Pixel(pixel, height)
{
    translate([ -Epsilon / 2, -Epsilon / 2, -Epsilon / 2 ]) cube([ pixel + Epsilon, pixel + Epsilon, height + Epsilon ]);
}
