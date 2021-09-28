import cv2
from torch._C import default_generator

class buttons():

    #creates buttons
    def __init__(self, position: tuple, button_type: str):
        self.position = position
        self.button_type = button_type
        self.axesLength  = (50, 25)
        self.time_pressed = 0
        self.defaulf_color = (0, 0, 255)
        self.current_color = self.defaulf_color

    #draw buttons on frames
    def draw_button(self, image):

        x = self.position[1]
        y = self.position[0]

        axesLength = self.axesLength

        center_coordinates = (x, y)
        angle              = 0
        startAngle         = 0
        endAngle           = 360
        color              = self.current_color
        thickness          = -1

        image = cv2.ellipse(image, center_coordinates, axesLength,
                angle, startAngle, endAngle, color, thickness)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        fontScale              = 1
        fontColor              = (255,0,0)
        lineType               = 2
        thickness              = 2

        (label_width, label_height), baseline = cv2.getTextSize(self.button_type, font, fontScale, thickness)
        co_ord                                = (self.position[1]-label_width//2, self.position[0]+label_height//2)

        cv2.putText(image, self.button_type, 
            co_ord, 
            font, 
            fontScale,
            fontColor,
            lineType)

        return image

    def is_pressed(self, index_fing_x, index_fing_y):
        while self.position[1]-self.axesLength[0]<=index_fing_x<=self.position[1] + self.axesLength[0] \
            and self.position[0]-self.axesLength[1]<=index_fing_y<=self.position[0] + self.axesLength[1]:
            self.time_pressed += 1
            self.current_color = (0, 255, 255)
            if self.time_pressed >= 15:
                return True
            else:
                return False
        self.time_pressed = 0
        self.current_color = self.defaulf_color