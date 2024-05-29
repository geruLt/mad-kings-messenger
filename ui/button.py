from .ui_element import UIElement

import pygame

class UIButton(UIElement):
    '''Button UI element.'''
    def __init__(self, text, width, height, pos, elevation, color, shadow, hover, fontsize=50):
        super().__init__()

        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.color_shadow = shadow
        self.hover = hover
        self.clicked = False
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = shadow
        font = pygame.font.SysFont('rockwell', fontsize)
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw_button(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 20
        bottom_rect.y += 20
        if top_rect.collidepoint(pos):
            self.top_color = self.color
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                bottom_rect.inflate_ip(self.elevation, self.elevation)
                top_rect.inflate_ip(self.elevation, self.elevation)

            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            self.top_color = self.hover
        else:
            self.top_color = self.color

        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color, (0, 0, *top_rect.size), border_radius = 12)
        screen.blit(top_surf, top_rect.topleft)

        screen.blit(self.text_surf, self.text_rect)
        return action