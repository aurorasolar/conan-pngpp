#include <cassert>
#include <iostream>
#include <png++/png.hpp>

using png_t = png::image< png::rgb_pixel >;

int main() {
    png_t image(128, 128);
    for (png::uint_32 y = 0; y < image.get_height(); ++y)
    {
        for (png::uint_32 x = 0; x < image.get_width(); ++x)
        {
            image[y][x] = png::rgb_pixel(x, y, x + y);
            // non-checking equivalent of image.set_pixel(x, y, ...);
        }
    }
    image.write("rgb.png");
    png_t im("rgb.png");
    return 0;
}
