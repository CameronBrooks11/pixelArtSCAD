// colormap.scad

// Define color map with RGB values between 0 and 255
colorMap255 = [
    ["0", [0, 0, 0]],         // Black
    ["1", [255, 215, 0]],     // Gold
    ["%", [255, 240, 245]],   // LavenderBlush
    ["B", [0, 0, 0]],         // Black
    ["W", [255, 255, 255]],   // White
    ["R", [255, 0, 0]],       // Red
    ["G", [0, 255, 0]],       // Green
    ["P", [255, 192, 203]],   // Pink
    ["V", [120, 81, 169]],    // Royal Purple
    ["Y", [255, 255, 0]],     // Yellow
    ["O", [255, 165, 0]],     // Orange
    ["C", [0, 255, 255]],     // Cyan
    ["M", [255, 0, 255]],     // Magenta
    ["N", [0, 0, 128]],       // Navy
    ["L", [50, 205, 50]],     // Lime
    ["D", [169, 169, 169]],   // DarkGray
    [" ", [255, 215, 0]]      // Default [Gold for space]
];

// Function to normalize RGB values to the range 0-1
function normalizeColor(rgb) = [rgb[0] / 255, rgb[1] / 255, rgb[2] / 255];

// Create a normalized color map (scaled to 0-1) from colorMap255
colorMap = [
    for (entry = colorMap255) 
    [entry[0], normalizeColor(entry[1])]
];

echo(colorMap);