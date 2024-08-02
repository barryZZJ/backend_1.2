from PIL import Image, ImageFilter


def gaussian_blur(image: Image.Image, radius: float = 2):
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def gaussian_blur_region(image: Image.Image, region_x, region_y, region_w, region_h, radius: float = 5):
    x, y, w, h = region_x, region_y, region_w, region_h
    region = image.crop((x, y, x + w, y + h))
    region = gaussian_blur(region, radius)
    image.paste(region, (x, y, x + w, y + h))
    return image


if __name__ == '__main__':
    input_image_path = '../src/images/lena.jpg'
    original_image = Image.open(input_image_path)

    # Choose parameters for each effect
    gaussian_blur_radius = 5
    rectangle_range = (230, 240, 115, 130)  # Example rectangle range (x, y, width, height)

    # Apply each effect
    region_gaussian_blurred_image = gaussian_blur_region(original_image.copy(), *rectangle_range, gaussian_blur_radius)

    # Save the results
    region_gaussian_blurred_image.save("../src/images/region_gaussian_blurred_image.jpg")
