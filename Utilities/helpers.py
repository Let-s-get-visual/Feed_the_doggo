import mediapipe as mp
import cv2
import numpy as np


def hand_center(h_landmarks, img):

    x = [landmark.x for landmark in h_landmarks.landmark]
    y = [landmark.y for landmark in h_landmarks.landmark]

    center = np.array([np.mean(x) * img.shape[1], np.mean(y) * img.shape[0]]).astype('int32')

    return center

# def reinit(item):
#     item.__init__((0, 0), item.item_type, item.item_id, new_instance=False)

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

