from imageio import imread
from numpy import sum, average


def to_grayscale(arr):
    """
    Convert color image to grayscale
    :param arr: 3d array
    :return: 3d array
    """
    if len(arr.shape) == 3:
        return average(arr, -1)  # average rgb channels over the last axis
    else:
        return arr


def normalize(arr):
    """
    Normalize to compensate for variations in exposure
    :param arr: 3d array
    :return: 3d array
    """
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng


def get_score(img1, img2):
    """
    Returns similarity score for 2 images
    :param img1: a file path to an image
    :param img2: a file path to an image
    :return: Similarity score (manhattan norm per pixel)
    """
    img1 = normalize(to_grayscale(imread(img1).astype(float)))
    img2 = normalize(to_grayscale(imread(img2).astype(float)))
    diff = img1 - img2
    manhattan_norm = sum(abs(diff))
    return manhattan_norm/img1.size



