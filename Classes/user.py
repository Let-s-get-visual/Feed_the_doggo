from pet_food import Pet_food
import numpy as np

class User:

    def __init__(self, user_name: str):
        self.status = 'human'
        self.score = 0
        self.lifes = 3
        self.user_name = user_name
        self.food = 'none'
        self.life_color = Pet_food.BRIGHT_GREEN

    def get_user_status(self):
        return self.status
    
    def status_changer(self, prediction):
        if prediction == 0:
            self.status = 'dog'
            self.food = 'bone'
        elif prediction == 1:
            self.status = 'fish'
            self.food = 'worm'
        elif prediction == 2:
            self.status = 'rabbit'
            self.food = 'carrot'
        elif prediction == -1:
            self.status = 'human'
        else:
            self.status = 'wait'
    
    def score_changer(self, item):
        if item.current_status < 0:
            if self.status == 'dog' and item.item_type == 'bone' or \
            self.status == 'fish' and item.item_type == 'worm' or \
            self.status == 'rabbit' and item.item_type == 'carrot':
                self.score += 1
            elif item.item_type == 'concrete':
                self.lifes -= 1
            else:
                self.score -= 1
        if self.score < 0:
            self.lifes -= 1
            self.score = 0
    
    def check_food(self, food_list):
        if self.status != 'human' and self.food not in food_list:
            self.status = 'wait'

        # print(self.status != 'human' and self.food not in food_list, self.status, 'merdazza!')
    
    def check_lifes(self):
        if self.lifes < 2:
            self.life_color = Pet_food.RED
    
    def user_reset(self):
        self.status = 'wait'
        self.score = 0
        self.lifes = 3
        self.food = 'none'
        self.life_color = Pet_food.BRIGHT_GREEN

        





    
