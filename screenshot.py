from PIL import ImageGrab
import win32gui

toplist, winlist = [], []
compass_path = r"project_images\screenshots\compass.png"
search_path = r"project_images\screenshots\search_square.png"
location_size = 50
compass_size = 80

crops = {
    "chrome_nmpz": (586, 156, 1390, 960),
    "chrome_nmpz_fullscreen": (555, 87, 1433, 965)
}

compass_crops = {
    "chrome_nmpz": (23, 891, 73, 941),
    "chrome_nmpz_fullscreen": (23, 931, 73, 981)
}


def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_screenshot():
    win32gui.EnumWindows(enum_cb, toplist)

    geo_window = [(hwnd, title) for hwnd, title in winlist if 'a diverse world - game - geoguessr' in title.lower()]
    # just grab the hwnd for first window matching firefox
    geo_window = geo_window[0]
    hwnd = geo_window[0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    # img.show()
    return img


def save_crops(mode):
    """
    Saves images of game location and compass
    :param mode: regions to crop
    :return: n/a
    """
    #im = get_screenshot()
    im = ImageGrab.grab()

    # Save image of location
    crop_region = crops[mode]
    crop_im = im.crop(crop_region)
    crop_im = crop_im.resize((location_size, location_size))
    crop_im.save(search_path)

    # Save image of compass
    compass_region = compass_crops[mode]
    compass_im = im.crop(compass_region)
    compass_im = compass_im.resize((compass_size, compass_size))
    compass_im.save(compass_path)

    im.close()
