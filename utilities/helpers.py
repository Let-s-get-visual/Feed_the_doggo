import mediapipe as mp
import cv2
import numpy as np


def hand_center(h_landmarks, img):

    x = [landmark.x for landmark in h_landmarks.landmark]
    y = [landmark.y for landmark in h_landmarks.landmark]

    center = np.array([np.mean(x) * img.shape[1], np.mean(y) * img.shape[0]]).astype('int32')

    return center

def food_left(food, food_list):
    if food.current_status > 0:
        food_list.append(food.item_type)

def set_position(img):
    rnd = np.random.randint(0, 39)
    corner = rnd % 4

    if corner == 0:
        pos = (0, 0)
    elif corner == 1:
        pos = (0, img.shape[1])
    if corner == 2:
        pos = (img.shape[0], 0)
    else:
        pos = (img.shape[0], img.shape[1])
    
    return pos

def black(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = (5, 5)

    mask = img > 70
    img[mask] = 255

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    dilated = cv2.dilate(closing, kernel, iterations=10)
    dilated = cv2.resize(dilated, (32, 32))

    return dilated

def bbox_landmarks(hn_landmark, image):
    padding = 20
    crop_copy = image.copy()

    x = [landmark.x for landmark in hn_landmark.landmark]
    y = [landmark.y for landmark in hn_landmark.landmark]

    coords = [min(x) * image.shape[1], max(x) * image.shape[1], min(y) * image.shape[0], max(y) * image.shape[0]]
    center = np.array([np.mean(x) * image.shape[1], np.mean(y) * image.shape[0]]).astype('int32')

    dist = [center[0] - coords[0], coords[1] - center[0], center[1] - coords[2], coords[3] - center[1]]
    bb_dim = int(max(dist) + padding)

    start_r = center[1] - bb_dim
    start_c = center[0] - bb_dim
    end_r = center[1] + bb_dim
    end_c = center[0] + bb_dim

    if start_r != 0 or start_c != 0:
        crop = crop_copy[start_r:end_r, start_c:end_c]
    elif start_r < 0 and start_c < 0:
        crop = crop_copy[:end_r, :end_c]

    return crop

