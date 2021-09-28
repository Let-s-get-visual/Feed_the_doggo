import numpy as np
import cv2

from typing import Tuple

class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class Pet_food(metaclass = IterRegistry):

    __metaclass__ = IterRegistry
    _registry = []

    # Colors defined in BGR
    GRAY = (50, 50, 50)
    WHITE = (255, 255, 255)
    ORANGE = (0, 153, 255)
    GREEN = (63, 140, 58)
    BRIGHT_GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    RED = (0, 0, 255)
    PINK = (137, 137, 250)

    # Other useful staff
    FONT = cv2.QT_FONT_NORMAL

    # Creates food item
    def __init__(self, position: tuple, item_type: str, item_id: int, new_instance=True):
        if new_instance:
            self._registry.append(self)
        self.position = position
        self.item_type = item_type
        self.item_id = item_id
        if item_type == 'bone':
            self.color = Pet_food.WHITE
            self.default_status = 3
        elif item_type == 'carrot':
            self.color = Pet_food.ORANGE
            self.default_status = 2
        elif item_type == 'worm':
            self.color = Pet_food.PINK
            self.default_status = 1
        else:
            self.color = Pet_food.GRAY
            self.default_status = 0
        self.dimension = 30
        self.m = np.random.uniform(0, 2)
        self.b = self.position[0] - self.m * self.position[1]
        self.speed = np.random.randint(1, 4)
        self.current_status = self.default_status

    # draws the item on the frame
    def draw_food(self, image):
        x = self.position[1]
        y = self.position[0]

        if self.item_type == 'bone':
            start_x = x - self.dimension
            start_y = y - self.dimension//2
            w = self.dimension * 2
            h = self.dimension
            img = cv2.rectangle(image, (start_x, start_y), (start_x + w, start_y + h), self.color, -1)
            img = cv2.circle(img, (start_x, start_y), 15, self.color, -1)
            img = cv2.circle(img, (start_x + w, start_y), 15, self.color, -1)
            img = cv2.circle(img, (start_x, start_y + h), 15, self.color, -1)
            img = cv2.circle(img, (start_x + w, start_y + h), 15, self.color, -1)

        elif self.item_type == 'carrot':
            ax1 = int(self.dimension * 0.66)
            ax2 = int(self.dimension * 1.5)
            leaves = np.array([[x - int(ax1 * 0.8), y - int(ax2 * 1.3)], [x + int(ax1 * 0.8), y - int(ax2 * 1.3)], [x, y - ax2 + 10]], np.int32)
            img = cv2.ellipse(image, (x, y), (ax1, ax2), 0, 0, 360, self.color, -1)
            cv2.drawContours(img, [leaves], 0, Pet_food.BRIGHT_GREEN, -1)

        elif self.item_type == 'worm':
            img = cv2.putText(image, 'S', (x - int(self.dimension), y + int(self.dimension)), Pet_food.FONT, 2.5, self.color, 8)
            img = cv2.circle(img, (x + 13, y - 18), 12, self.color, -1)
            img = cv2.circle(img, (x + 10, y - 23), 2, Pet_food.BLACK, -1)
            img = cv2.circle(img, (x + 16, y - 23), 2, Pet_food.BLACK, -1)
            img = cv2.ellipse(img, (x + 13, y - 16), (4,4), 0, 180, 0, Pet_food.BLACK, 2)
            
        else:
            img = cv2.rectangle(image, (self.position[1] - self.dimension, self.position[0] - self.dimension),
            (self.position[1] + self.dimension, self.position[0] + self.dimension),
            self.color, -1)
        
        return img
    
    # updates item's position (linear movement)
    def move_food(self):
        pos = list(self.position)
        pos[1] += self.speed
        pos[0] = int(self.m * self.position[1] + self.b)
        self.position = tuple(pos)

    # detects the window edges
    def detect_edge(self, img):
        pos = list(self.position)
        if pos[0] > img.shape[0]:
            pos[0] = pos[0] - 3
            self.m = -1 * self.m
            self.b = pos[0] - self.m * pos[1]
        elif pos[1] > img.shape[1]:
            self.speed = -self.speed
            self.m = -self.m
            self.b = pos[0] - self.m * pos[1]
        elif pos[0] < 0:
            pos[0] = -pos[0]
            self.m = -self.m
            self.b = pos[0] - self.m * pos[1]
        elif pos[1] < 0:
            pos[1] = - pos[1]
            self.speed = -self.speed
            self.m = -self.m
            self.b = pos[0] - self.m * pos[1]
        
        self.position = tuple(pos)
    
    # detects hand collision
    def hand_collision(self, hand_center: tuple):
        collision_radius = 30
        dst = np.sqrt((self.position[1] - hand_center[0])**2 + (self.position[0] - hand_center[1])**2)

        if dst <= collision_radius:
            self.current_status -= 4
    
    def reinit(self, pos):
        self.__init__(pos, self.item_type, self.item_id, new_instance=False)
