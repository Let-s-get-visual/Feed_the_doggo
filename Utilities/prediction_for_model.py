import torch
import torch.nn.functional as F
import cv2
import numpy as np
from statistics import mode

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

    kernel = (5, 5)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = image > 70
    image[mask] = 255
    # inverted = 255 - gray
    #
    # blurred = cv2.GaussianBlur(inverted, kernel, 0)
    #
    # canny = cv2.Canny(blurred, 100, 200)
    #
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    #
    dilated = cv2.dilate(closing, kernel, iterations=20)
    #
    # dilated = dilated.reshape(255, 255, 1)
    #
    # stacked = np.dstack((image, dilated))

    return dilated


def predict(hn_landmark, image, model):

    model.eval()

    cropped_image = bbox_landmarks(hn_landmark, image)
    stacked = add_dim(cropped_image)

    tensor_stacked = F.normalize(torch.from_numpy(stacked).float())
    outputs = model(tensor_stacked.view(-1, 4, 255, 255))
    probs = F.log_softmax(outputs)
    pred = torch.argmax(probs)

    return pred


img = cv2.imread("images/train/dog/1625670216.990446_dilan.png", 0)

image = add_dim(img)

cv2.imshow('test', image)
cv2.waitKey()
cv2.destroyAllWindows()










