
#NEEDED IMPORTS
#######################################################################################################################################
import torch
import torchvision
import time
import cv2

import numpy as np
import mediapipe as mp

from statistics import mode

from classes.pet_food import Pet_food
from classes.user import User
# from client import send_data
# from client_preprocessing import black, bbox_landmarks
from model.prediction import predict

import utilities.helpers as hp
import utilities.prediction_for_model as pfm
import utilities.animal_figures as af
import classes.handtracking as ht
from classes.menu_buttons import buttons
from GUI.play_button import play
import statistics

#######################################################################################################################################



def gui():

    # USEFUL VARIABLES
    global_time = time.time()
    window = 'Interactive games'
    game_status = 0 
    sleep_timer = 0

    # Media_pipe requirements
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    player = User('test')
    detector=ht.handDetector(detectionCon=0.8)

    FRAME_COUNTER = 5
    PREDICTION_LIST = []
    state = 'idle'
    player.status = 'wait'

    # Access to webcam
    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        response, frame = vc.read()
    else:
        response = False

    #call the class by giving dimensions and name of the buttons
    Start = buttons((frame.shape[0]//4, frame.shape[1]//2), 'Start')
    Help = buttons((frame.shape[0]//4+80, frame.shape[1]//2), 'Help')
    Exit = buttons((frame.shape[0]//4+160, frame.shape[1]//2), 'Exit')

########################################### Code to record a video ###########################################
    # out_vid = cv2.VideoWriter('./output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (640, 480))
########################################### Code to record a video ###########################################

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
        while response:
            response, frame = vc.read()
            # frame_n=cv2.flip(frame,4)
                        
            image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            img_n=detector.findHands(image)
            

            results = hands.process(image)


            list=detector.findPosition(img_n,draw=False)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                image_height, image_width, image_depth = image.shape

                for hand_landmarks in results.multi_hand_landmarks:
                    index_fing_x, index_fing_y = (hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width,
                                                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)

                    hc = hp.hand_center(hand_landmarks, image)

                    blank = np.zeros((image_height, image_width, image_depth), dtype=np.uint8)
                    mp_drawing.draw_landmarks(blank, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    if state == 'predict' and FRAME_COUNTER > 0:
                        
                        try:
                            blank = hp.bbox_landmarks(hand_landmarks, blank)
                            blank = hp.black(blank)

                            PREDICTION_LIST.append(blank)
                            FRAME_COUNTER -= 1
                        except:
                            continue

                    if len(PREDICTION_LIST) == 5:
                        PREDICTION_LIST = np.array(PREDICTION_LIST)

                        pred_list = []
                        for img in range(PREDICTION_LIST.shape[0]):
                            image = PREDICTION_LIST[img, :, :].reshape(1, 1, 32, 32)
                            pred_list.append(predict(image))
                        final_pred = str(statistics.mode(pred_list))

                        PREDICTION_LIST = []
                        FRAME_COUNTER = 5
                        state = 'idle'
                        player.status_changer(int(final_pred))
                
            try:
                # Master interface
                if game_status == 0:
                    
                    #draw the buttons 
                    Start.draw_button(image)
                    Help.draw_button(image)
                    Exit.draw_button(image)

                    #condition for index finger to touch play button
                    if Start.is_pressed(index_fing_x, index_fing_y):
                        first_time_pressed = True
                        game_status = 1

                    #condition for index finger to touch exit and Quit button
                    if Exit.is_pressed(index_fing_x, index_fing_y):
                        game_status = 99
                    
                    #condition for index finger to touch exit button
                    if Help.is_pressed(index_fing_x, index_fing_y):
                        game_status = 2

                # Playing interface
                if game_status == 1:

                    if player.status == 'wait':
                        starting_to_wait = True
                        player.status_changer(-1)
                    
                    if starting_to_wait:
                        waiting_time = time.time()
                        starting_to_wait = False

                    image, game_status, state, first_time_pressed = play(vc, response, hc, image, index_fing_x, index_fing_y, player, global_time, state, list, waiting_time, window, first_time_pressed) #play the game

                # Exit the game
                elif game_status == 99:
                    break

                # Help interface
                elif game_status == 2:
                    helpme = cv2.imread('GUI/Instructions.png')
                    sleep_timer += 1
                    cv2.imshow('help', helpme)

                    if sleep_timer == 180:
                        cv2.destroyWindow('help')
                        sleep_timer = 0
                        game_status = 0

                cv2.imshow(window, image)

                
            except:
                continue
########################################### Code to record a video ###########################################
            # out_vid.write(np.uint8(image))
########################################### Code to record a video ###########################################

            key = cv2.waitKey(1)
            if key == 27:
                break
    
########################################### Code to record a video ###########################################
    # out_vid.release()
########################################### Code to record a video ###########################################

    vc.release()

    cv2.destroyAllWindows()

