import pygame
from constants import WINDOW_HEIGHT,WINDOW_WIDTH
GUI_IMAGE_SIZE = (40, 40)
SCROLL_IMAGE_SIZE = (40, 25)
GUI_IMAGE_MARGIN = 20
GUI_CORNER_OFFSET = 10
GUI_NUMBER_FONT_SIZE = 24
GUI_NUMBER_FONT_COLOR = (255, 255, 255)
LABEL_FONT_SIZE = 10
LABEL_FONT_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
FONT_PATH = pygame.font.match_font("arial")
IMAGE_PATHS = ['assets/gui_circle.png','assets/gui_scroll.png']
class Element:

    def __init__(self,manager,text,value):
        self.images = []
        for path in IMAGE_PATHS:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.smoothscale(image,GUI_IMAGE_SIZE)
            self.images.append(image)
        positions = self.calc_positions(self.images[0])
        self.position = positions[text]
        self.text = text
        self.manager = manager
        self.label = self.get_label(LABEL_FONT_SIZE,LABEL_FONT_COLOR,text)
        self.label_position = self.get_label_position(self.label,self.images[1])
        self.label_position = self.label_position[0],self.label_position[1] - GUI_IMAGE_MARGIN

        self.value_label = self.get_label(GUI_NUMBER_FONT_SIZE,GUI_NUMBER_FONT_COLOR,str(value))
        self.value_label_position = self.get_label_position(self.value_label,self.images[0])

    
    def get_label(self,font_size,font_color,text):
        font = pygame.font.Font(FONT_PATH, font_size)
        label = font.render(text, True, font_color)
        return label

    def get_label_position(self,label,base_image):
        x = self.position[0] + base_image.get_width() // 2 - label.get_width() // 2
        y = self.position[1] + base_image.get_height() // 2 - label.get_height() //2
        return x,y
        
    def refresh(self,window):
        if self.text == "Actions":
            self.value = self.manager.current_player.actions
        elif self.text == "Buys":
            self.value = self.manager.current_player.buys
        elif self.text == "Player":
            self.value = self.manager.current_player.name
        else:
            self.value = self.manager.current_player.treasure
        self.value_label = self.get_label(GUI_NUMBER_FONT_SIZE,GUI_NUMBER_FONT_COLOR,str(self.value))
        self.draw(window)
    
    def draw(self,window):
        window.blit(self.images[0],self.position)
        window.blit(self.images[1],(self.position[0],self.position[1] - self.images[0].get_height()/2))
        window.blit(self.label,self.label_position)
        window.blit(self.value_label,self.value_label_position)

    def calc_positions(self,image):
        positions = {}
        positions["Actions"] = (WINDOW_WIDTH - GUI_CORNER_OFFSET - image.get_width(),
                WINDOW_HEIGHT - GUI_CORNER_OFFSET - image.get_height())
        positions["Buys"] = positions["Actions"][0],positions["Actions"][1] - image.get_height() - GUI_IMAGE_MARGIN
        positions["Treasure"] = positions["Actions"][0] - image.get_width() - GUI_IMAGE_MARGIN, positions["Actions"][1]
        positions["Player"] = positions["Actions"][0] - image.get_width() - GUI_IMAGE_MARGIN, positions["Actions"][1] - image.get_height() - GUI_IMAGE_MARGIN
        return positions