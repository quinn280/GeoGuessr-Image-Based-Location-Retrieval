import cv2 as cv
import numpy as np
from skimage.transform import rotate

PRECISION_THRESHOLD = 0.5  # Increment of desired precision. Lower than 0.5 has diminishing returns.
TEMPLATE_PATH = r"project_images\templates\compass template.png"


# Derive compass template in preparation for template matching
compass_template = cv.imread(TEMPLATE_PATH)
compass_template = cv.cvtColor(compass_template, cv.COLOR_BGR2BGRA)
blend = cv.addWeighted(compass_template[:, :, :3], 0.5, cv.flip(compass_template[:, :, :3], 0), 0.5, 0)
compass_template[:, :, 3] = cv.cvtColor(blend, cv.COLOR_BGR2GRAY)
compass_template[:, :, 3] = cv.threshold(compass_template[:, :, 3], 254, 255, cv.THRESH_BINARY_INV)[1]


def get_best_angle(angles, img):
    """
    Calculates template match score for given angles and returns the best match and its score.
    :param angles: a list of angles to score
    :param img: an opencv image object of compass
    :return: a tuple of the best matching angle and its match score
    """
    # Iterate through range of angles
    scores = []
    for angle in angles:
        # Calculate score and append to score list
        scores.append(get_angle_score(angle, img))

    # Get index of the lowest score
    min_index = np.argmin(scores)

    # Find best match angle (the lowest score is best match)
    return angles[min_index], scores[min_index]


def get_angle_score(angle, img):
    """
    Gets template matching score for angle. Lower scores mean a better match.
    :param angle: an angle
    :param img: an opencv image object of compass
    :return: The match score for the angle
    """
    # Rotate compass and mask
    compass_rot = rotate(compass_template.copy(), angle, resize=True).astype(np.float32)

    # Template matching
    result = cv.matchTemplate(img, compass_rot[..., :3], cv.TM_SQDIFF, mask=compass_rot[..., 3])

    # Return Score
    return cv.minMaxLoc(result)[0]


def estimate_heading(compass_path):
    """
    Estimates heading by using multiple calls directly or indirectly to template matching functions.
    Algorithm optimizes for the minimum number of template matches because they are computationally intensive.
    :param compass_path: file path to image of compass
    :return: estimated heading
    """
    img = cv.imread(compass_path).astype(np.float32) / 255

    # Find best match within +/- 20 degrees. Template matching scores do not continuously increase from final estimate
    # until within this range. Ex. if compass is at 0 then 180 may score lower than 30 even though it is further.
    step = 20
    mid_ang, mid_sco = get_best_angle(range(0, 360, step), img)

    # Ternary Search Algorithm. Divides search range in half on each iteration. For a given range compares 1/4, 1/2,
    # and 3/4 markers. If 1/4 is the min, 0-1/2 is the new range. If 1/2 is the min, 1/4-3/4 is the new range. If 3/4
    # is the min, 1/2-1 is the new range. Iterates until desired precision is met. This algorithm is able to cut the
    # search range in half with only 1-2 template matching calls.
    while step > PRECISION_THRESHOLD:
        # Divide range in half and update new start and end markers
        step /= 2
        start_ang, end_ang = mid_ang - step, mid_ang + step

        # If start < mid, make start the new middle. Note: Prevents calculating score for end if unnecessary
        start_sco = get_angle_score(start_ang, img)
        if start_sco < mid_sco:
            mid_ang, mid_sco = start_ang, start_sco

        # If end < mid, make end the new middle. If not, keep mid as is.
        else:
            end_sco = get_angle_score(end_ang, img)
            if end_sco < mid_sco:
                mid_ang, mid_sco = end_ang, end_sco

    # '% 360' converts negative angles and 360+ angles to 0-360
    return mid_ang % 360
