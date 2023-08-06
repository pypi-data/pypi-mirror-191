from jcopvision.utils import normalize_pixel


def enhance_brightness(image, gain=10):
    image = normalize_pixel(image)
    gain /= 255
    new_image = image + gain
    return new_image.clip(0, 1)


def enhance_contrast(image, gain=10):
    image = normalize_pixel(image)
    gain = 1 + gain / 100
    new_image = image * gain
    return new_image.clip(0, 1)
