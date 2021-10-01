from classes.pet_food import Pet_food
from classes.menu_buttons import buttons
import mediapipe as mp
import numpy as np
import utilities.helpers as hp
import time
import cv2

import utilities.prediction_for_model as pfm
import utilities.animal_figures as af
import classes.handtracking as ht

from classes.user import User

#call the class to create the food
bone = Pet_food((1, 100), 'bone', 0)
bone1 = Pet_food((1, 100), 'bone', 4)
carrot = Pet_food((1, 200), 'carrot', 1)
carrot1 = Pet_food((1, 200), 'carrot', 5)
concrete = Pet_food((1, 400), 'concrete', 2)
worm = Pet_food((0, 300), 'worm', 3)
worm1 = Pet_food((0, 300), 'worm', 6)

Quit = buttons((40, 60), 'Quit')

# Useful Vars
fontScale = 0.7
thickness = 2
CHANGE_INTERVAL = 3

def play(cap, response, hc, image, index_fing_x, index_fing_y, player, global_time, state, list, waiting_time, window, first_time_pressed):
        
    ################################################################################################################################################
    Quit.draw_button(image)

    if Quit.is_pressed(index_fing_x, index_fing_y):
        game_status = 0
    else:
        game_status = 1
    
    if first_time_pressed:
        for food in Pet_food:
            pos = hp.set_position(image)
            food.reinit(pos)
        player.user_reset()
        first_time_pressed = False

    try:
        if player.status == 'human' and (time.time() - waiting_time) < CHANGE_INTERVAL:

            cd_scale = (time.time() - waiting_time - (time.time() - waiting_time)//1) * 4
            text = str(CHANGE_INTERVAL - int((time.time() - waiting_time)//1))
            (w_cd, h_cd), bl_cd = cv2.getTextSize(text, Pet_food.FONT, cd_scale, thickness)
            
            txt_scale = 1.5
            (w_txt, h_txt), bl_txt = cv2.getTextSize('Prepare a gesture', Pet_food.FONT, txt_scale, thickness)

            image = cv2.putText(image, 'Prepare a gesture', (image.shape[1]//2 - w_txt//2, image.shape[0]//3),
                    Pet_food.FONT, txt_scale, Pet_food.RED, thickness, cv2.LINE_AA)


            image = cv2.putText(image, str(CHANGE_INTERVAL - int((time.time() - waiting_time)//1)),
                                (image.shape[1]//2 - w_cd//2, image.shape[0]//2 + h_cd//2),
                                Pet_food.FONT, cd_scale, Pet_food.RED, thickness, cv2.LINE_AA)

        else:
            if player.status == 'human':
                state = 'predict'

        # Checks how many pet food are left
        food_list = []

        for food in Pet_food:
            hp.food_left(food, food_list)
                
        player.check_food(food_list)
        player.check_lifes()

        # Draw the predicted character
        ##############################################################################################################
        try:
            if player.status == 'dog':
                af.draw_dog(list, image)
            elif player.status == 'fish':
                af.draw_fish(list, image)
            elif player.status == 'rabbit':
                af.draw_rabbit(list, image)
        except:
            pass
        ##############################################################################################################
        
        #  updates the item's position
        for food in Pet_food:
            if food.current_status >= 0:
                food.move_food()

        #  draws the item in new position
        for food in Pet_food:
            if food.current_status >= 0:
                image = food.draw_food(image)

        # if the item reach the window's edge it bounces back
        for food in Pet_food:
            if food.current_status >= 0:
                food.detect_edge(image)

        # checks if you eat the item and updates score and lifes
        if player.get_user_status() != 'human' and player.get_user_status() != 'wait':
            for food in Pet_food:
                if food.current_status >= 0:
                    food.hand_collision(hc)
                    player.score_changer(food)

        # checks if all the items were eaten
        if np.array([item.current_status<0 for item in Pet_food if item.item_type != 'concrete']).all():
            player.status = 'wait'
            for food in Pet_food:
                if food.item_type != 'concrete':
                    food.reinit(hp.set_position(image))
        elif concrete.current_status < 0:
            concrete.reinit(hp.set_position(image))

        # Print out lifes left and score
        ############################################################################################################################################

        if player.life_color == Pet_food.BRIGHT_GREEN or int(time.time() - global_time) % 2 == 1:
            image = cv2.putText(image, 'lifes: ' + str(player.lifes), (image.shape[1] - 120, 20), Pet_food.FONT, fontScale, player.life_color, thickness)
        image = cv2.putText(image, 'Score: ' + str(player.score), (image.shape[1] - 120, 50), Pet_food.FONT, fontScale, Pet_food.GREEN, thickness)

        ############################################################################################################################################
       
        if player.lifes <= 0:
            game_status = 0

    # TEST PURPOSE ONLY!!!!!!!!!!
    ##############################################################################################################################################
        # elif key == ord('d') or key == ord('D'):
        #     player.status_changer(0)
        # elif key == ord('f') or key == ord('F'):
        #     player.status_changer(1)
        # elif key == ord('r') or key == ord('R'):
        #     player.status_changer(2)
        # elif key == ord('h') or key == ord('H'):
        #     player.status_changer(-1)
        # elif key == ord('w') or key == ord('W'):
        #     player.status_changer(5)
    ##############################################################################################################################################
        
    except:
        pass

    return image, game_status, state, first_time_pressed