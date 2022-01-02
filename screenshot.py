from PIL import ImageGrab

COMPASS_PATH = r"project_images\screenshots\compass.png"
SEARCH_PATH = r"project_images\screenshots\search_square.png"
LOCATION_SIZE = 50
COMPASS_SIZE = 80


def save_crops():
    """
    Saves images of game location and compass
    :return: n/a
    """
    # im = get_screenshot()
    im = ImageGrab.grab()

    # Save image of location
    width, height = im.size
    start_x = int((555 / 1920) * width)  # Fractions are from original aspect ratio of location database
    start_y = int((87 / 1080) * height)
    square_length = int((878 / 1920) * width)
    crop_region = (start_x, start_y, start_x + square_length, start_y + square_length)
    crop_im = im.crop(crop_region)
    crop_im = crop_im.resize((LOCATION_SIZE, LOCATION_SIZE))
    crop_im.save(SEARCH_PATH)

    # Save image of compass
    compass_region = (23, height - 149, 73, height - 99)  # Compass is fixed distance from bottom left corner
    compass_im = im.crop(compass_region)
    compass_im = compass_im.resize((COMPASS_SIZE, COMPASS_SIZE))
    compass_im.save(COMPASS_PATH)

    im.close()
