import pygame
from constants import WINDOW_WIDTH,FONT_PATH,BLACK,GRAY
class Option:
    def __init__(self,text,position):
        self.text = text
        self.position = position
        self.label = pygame.font.Font(FONT_PATH,30).render(text, True, BLACK,GRAY)
        self.rect = pygame.Rect(position[0],position[1],self.label.get_width(),self.label.get_height())
    
    def draw(self,window):
        window.blit(self.label,self.position)
