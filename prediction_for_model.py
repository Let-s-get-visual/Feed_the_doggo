import torch
import torch.nn.functional as F
import cv2
import numpy as np
from statistics import mode

model = torch.load('saved_models/best_acc_model.pth', map_location='cpu')


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


def add_dim(image):

    kernel = (3, 3)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    inverted = 255 - gray

    blurred = cv2.GaussianBlur(inverted, kernel, 0)

    canny = cv2.Canny(blurred, 100, 200)

    closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)

    dilated = cv2.dilate(closing, kernel, iterations=4)

    dilated = dilated.reshape(255, 255, 1)

    stacked = np.dstack((image, dilated))

    return stacked


def predict(hn_landmark, image, model):

    model.eval()

    cropped_image = bbox_landmarks(hn_landmark, image)
    stacked = add_dim(cropped_image)

    tensor_stacked = F.normalize(torch.from_numpy(stacked).float())
    outputs = model(tensor_stacked.view(-1, 4, 255, 255))
    probs = F.log_softmax(outputs)
    pred = torch.argmax(probs)

    return pred


""" 
The code for time series smoothing
"""
FRAME_COUNTER = 20
predictions_list = []

state = 'idle'

if state == 'predict' and FRAME_COUNTER > 0:
    predictions_list.append(predict())
    FRAME_COUNTER -= 1

else:
    final_pred = mode(predictions_list)
    predictions_list = []
    FRAME_COUNTER = 20
    state = 'idle'










