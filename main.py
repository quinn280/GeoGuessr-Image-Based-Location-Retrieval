import time
import keyboard
import pyinputplus as pyip
import screenshot
import CBIR
import os
import compass

#location_folder = r"project_images\adw location images"
location_folder = r"C:\Users\quinn\OneDrive\Pictures\CBIRhub\World 50"
compass_path = r"project_images\screenshots\compass.png"
search_path = r"project_images\screenshots\search_square.png"
mode = "chrome_nmpz"
cbir_threshold = 15


class Location:
    """
    This class represents a single location
    """

    # Static Variable, Estimated Heading
    estimated_heading = 1000

    def __init__(self, latitude, longitude, heading, file_path):
        """
        This is the initializer for location class.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.file_path = file_path

        self.proximity = 1000
        self.CBIR_score = 1000

    def coordinate_str(self):
        return f"{self.latitude}, {self.longitude}"

    def location_str(self):
        ...  # use geopy to return location string from coordinates

    def google_map_link(self):
        return f'https://maps.google.com/?q=' \
               f'{self.latitude},{self.longitude}&ll={self.latitude},{self.longitude}&z=7'

    def update_proximity(self):
        """
        Calculates and updates new proximity value with the class variable estimated heading
        """
        self.proximity = abs(self.heading - Location.estimated_heading) % 360
        if self.proximity > 180:
            self.proximity = 360 - self.proximity

    def reset(self):
        """
        Resets proximity and CBIR score
        """
        self.proximity = 1000
        self.CBIR_score = 1000

    def __str__(self):
        """
        Return a str that that shows all location info.
        """
        return f"Coordinates: {self.coordinate_str()}\nCBIR Score: {self.CBIR_score:.2f}. " \
               f"Proximity: {self.proximity:.2f}. Estimated Heading: {Location.estimated_heading:.2f}. " \
               f"Actual Heading: {self.heading:.2f}.\nGoogle Map Link: {self.google_map_link()}\n"


def set_up(loc_folder):
    """
    Creates list of location objects from folder of images. Filename of images contains location data.
    Filename format is 'lat, lon, head.png'  ex. '-0.006951711604243485, 35.58404885119737, 106.2760009765625.png'
    :param loc_folder: path to folder of location images
    :return: a list of location objects
    """
    location_list = []
    for filename in os.listdir(loc_folder):
        lat = float(filename.split(', ')[0])
        lon = float(filename.split(', ')[1])
        head = float(filename.split(', ')[2][:-4])  # [:-4] removes file extension '.png'

        file_path = os.path.join(loc_folder, filename)
        location_list.append(Location(lat, lon, head, file_path))

    return location_list


def find_location(location_list, search_range=4):
    """
    Prints information for game location if found
    :param location_list: a list of location objects
    :param search_range: range of proximity to compass estimation to search through
    :return: n/a
    """
    print("Searching....")
    start = time.perf_counter()

    # Screenshot game location
    screenshot.save_crops(mode)
    screenshot_time_stamp = time.perf_counter()

    # Calculate estimated compass heading
    Location.estimated_heading = compass.estimate_heading(compass_path)
    compass_time_stamp = time.perf_counter()

    # Calculate and update 'proximity' instant variables, then sort by proximity
    for loc in location_list:
        loc.update_proximity()
    location_list.sort(key=lambda x: x.proximity)
    update_and_sort_stamp = time.perf_counter()

    # Iterate through location objects until match is found or until end of search range
    search_count = 0
    for loc in location_list:
        # Calculate CBIR Score
        loc.CBIR_score = CBIR.get_score(search_path, loc.file_path)
        search_count += 1

        # If score is under threshold, print location information and exit loop
        if loc.CBIR_score < cbir_threshold:
            print('Match Found!\n')
            print(f"Searches: {search_count}")
            print(loc)
            break

        # If 'proximity' values reach end of search range, print 'No match' and exit loop
        if loc.proximity > (search_range / 2):
            print('No match\n')
            print(f"Estimated Heading: {Location.estimated_heading}")
            response = pyip.inputYesNo(prompt="(For Testing Purposes) Search for match?")
            if response == 'yes':
                filename = pyip.inputStr("Input Filename to search")
                file_path = os.path.join(location_folder, filename+".png")
                for loc2 in location_list:
                    if file_path == loc2.file_path:
                        loc2.CBIR_score = CBIR.get_score(search_path, loc2.file_path)
                        print(loc2)

            break

    end_time_stamp = time.perf_counter()
    screenshot_time = screenshot_time_stamp - start
    compass_time = compass_time_stamp - screenshot_time_stamp
    update_and_sort_time = update_and_sort_stamp - compass_time_stamp
    cbir_time = end_time_stamp - update_and_sort_stamp
    total_time = end_time_stamp - start
    print(f"Screenshot time: {screenshot_time:.2f}. Compass time: {compass_time:.2f}. "
          f"Update & Sort Time: {update_and_sort_time:.2f}. CBIR time: {cbir_time:.2f}. "
          f"Total duration: {total_time:.2f}\n")

    # Reset 'proximity' and 'CBIRscore' instance variables
    for loc in location_list:
        loc.reset()


def main():
    location_list = set_up(location_folder)
    print('Ready\n')

    while True:
        keyboard.wait('3')
        find_location(location_list, search_range=5)


if __name__ == '__main__':
    main()
