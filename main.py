import keyboard
import pyinputplus as pyip
import screenshot
import CBIR
import os
import compass
import pyperclip
from location import Location
from timelog import TimeLog

# Global Variables
COMPASS_PATH = r"project_images\screenshots\compass.png"
SEARCH_PATH = r"project_images\screenshots\search_square.png"
SS_MODE = "chrome_nmpz_laptop_fullscreen"
CBIR_THRESHOLD = 15
PROX_RANGE = 5


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


def find_location(location_list):
    """
    Prints information for game location if found
    :param location_list: a list of location objects
    :return: n/a
    """
    print("\nSearching....")
    time_log = TimeLog()

    # Screenshot game location
    screenshot.save_crops()
    time_log.add_stamp("Screenshot")

    # Calculate estimated compass heading
    Location.estimated_heading = compass.estimate_heading(COMPASS_PATH)
    time_log.add_stamp("Compass")

    # Calculate and update 'proximity' instant variables, then sort by proximity
    for loc in location_list:
        loc.update_proximity()
    location_list.sort(key=lambda x: x.proximity)
    time_log.add_stamp("Update & Sort")

    # Iterate through location objects until match is found or until end of search range
    search_count = 0
    for loc in location_list:
        # Calculate CBIR Score
        loc.CBIR_score = CBIR.get_score(SEARCH_PATH, loc.file_path)
        search_count += 1

        # If score is under threshold, print location information and exit loop
        if loc.CBIR_score < CBIR_THRESHOLD:
            print('Match Found!\n')
            print(f"Searches: {search_count}")
            print(loc)
            pyperclip.copy(loc.google_map_link())
            break

        # If 'proximity' values reach end of search range, print 'No match' and exit loop
        if loc.proximity > (PROX_RANGE / 2):
            print('No match\n')
            print(f"Searches: {search_count}")
            print(f"Estimated Heading: {Location.estimated_heading}")
            pyperclip.copy('No match')
            # response = pyip.inputYesNo(prompt="(For Testing Purposes) Search for match?")
            # if response == 'yes':
            #     filename = pyip.inputStr("Input Filename to search")
            #     file_path = os.path.join(TEMP_LOCATION_FOLDER, filename+".png")
            #     for loc2 in location_list:
            #         if file_path == loc2.file_path:
            #             loc2.CBIR_score = CBIR.get_score(SEARCH_PATH, loc2.file_path)
            #             print(loc2)

            break

    # Display how long each portion of finding the location took
    time_log.add_stamp("CBIR")
    time_log.print()

    # Reset 'proximity' and 'CBIRscore' instance variables
    for loc in location_list:
        loc.reset()


def main():
    # Set up location list from location folder
    print("Important: Read User Guide in README file to ensure program runs successfully\n")
    location_folder = pyip.inputFilepath(prompt="Enter in path to directory of location images: ")
    print("Setting up...")
    location_list = set_up(location_folder)
    print('Ready')

    # Main Loop
    while True:
        keyboard.wait('3')
        find_location(location_list)


if __name__ == '__main__':
    main()
