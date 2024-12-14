include <colormap.scad> // Include the color map
include <pix00.scad>    // Import the default pixel art

//------------------------------------------------------------
// Parameters in millimeter
//------------------------------------------------------------
$fn = 150;           // OpenSCAD Resolution
Epsilon = 1 / 10000; // Small offset to avoid manifold issues
Thickness = 4;       // Pixel thickness
debug = false;

// Pixel Size
X = 10;
Y = X;
Z = X; // Pixel height. Set Z to 0 for flat pixels

//------------------------------------------------------------
// PixArt
//------------------------------------------------------------
module PixArt(H = Pix00)
{
    for (i = [0:len(H) - 1], j = [0:len(H[i]) - 1])
    {
        if (debug)
        {
            echo(str("\t i = ", i, "\t j = ", j, "\t H[i][j] = ", H[i][j], " "));
        }

        if (H[i][j] != " ")
        {
            P = getColor(H[i][j]);
            color(P) translate([ i * X, j * Y, 0 ]) Pixel();
            if (debug)
                echo("Put Pixel with Color = ", P);
        }
        else if (debug)
        {
            echo(str("nop - ", H[i][j]));
            color("grey", 0.5) translate([ i * X, j * Y, 0 ]) Pixel();
        }
    }
}

// Function to get color based on character using external map
function getColor(char) = let(index = searchIndex(char))(index == -1) ? "gold" : colorMap[index][1];

// Helper function to find the index of a character in the color map
function searchIndex(char, i = 0) = (i == len(colorMap)) ? -1 : (colorMap[i][0] == char) ? i : searchIndex(char, i + 1);

// The Pixel
module Pixel()
{
    translate([ -Epsilon / 2, -Epsilon / 2, -Epsilon / 2 ]) cube([ X + Epsilon, Y + Epsilon, Z + Epsilon ]);
}