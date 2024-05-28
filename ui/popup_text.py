from .ui_element import UIElement
from .button import UIButton

import pygame

class UIPopupText(UIElement):
    '''Popup Text UI element.'''
    def __init__(self, text, fontsize, text_box_props, textcolor, backgroundcolor, margin, spacing):
        super().__init__()

        # First render the text to an image, line by line
        self.text = text
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.margin = margin
        self.spacing = spacing
        self.font = pygame.font.SysFont('timesnewroman', fontsize)

        self.text_box = pygame.Rect(*text_box_props)
        # Set up the bounding box
        self.bounding_box = pygame.Surface((self.text_box.width, self.text_box.height))
        self.bounding_box.set_alpha(200)
        self.bounding_box.fill(backgroundcolor)

    def draw(self, screen, button=False, active=False, offset=0):
        # Render the bbox
        screen.blit(self.bounding_box, self.text_box)
        if active:
            pygame.draw.rect(screen,  pygame.Color('dodgerblue1'), self.text_box, 2)
        else:
            pygame.draw.rect(screen, self.backgroundcolor, self.text_box, 2)

        # Render the text
        paragraphs =  self.text.split('\n')
        x, y = self.text_box.x + 20 + offset , self.text_box.y + 20
        for par in paragraphs:
            words = [word.split(' ') for word in par.splitlines()]
            space = self.font.size(' ')[0]  # The width of a space.
            max_width, max_height = self.bounding_box.get_size()
            for line in words:
                for word in line:
                    word_surface = self.font.render(word, 1, self.textcolor)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = self.text_box.x + 20 + offset  # Reset the x.
                        y += word_height  # Start on new row.
                    screen.blit(word_surface, (x, y))
                    x += word_width + space
                x = self.text_box.x + 20 + offset # Reset the x.
                y += word_height  # Start on new row.
            # At the end of paragraph
            word_surface = self.font.render(' ', 1, self.textcolor)
            word_width, word_height = word_surface.get_size()
            screen.blit(word_surface, (x, y))
            x = self.text_box.x +  20  + offset  # Reset the x.
            y += word_height  # Start on new row.

        if button:
            self.button = UIButton(text="x",
                                 width=30,
                                 height=35,
                                 pos=(self.text_box.x + self.text_box.width - 40,
                                      self.text_box.y ),
                                 elevation=10,
                                 color = (128, 128, 128, 128),
                                 shadow=  (100, 100, 100, 128),
                                 hover=  (200, 200, 200, 128))
            self.button.draw_button(screen)

    def drawQuests(self, screen, quests, super_insults, insults, completed_quests, completed_super_insults, completed_insults):
        # Render the bbox
        screen.blit(self.bounding_box, self.text_box)
        pygame.draw.rect(screen, self.backgroundcolor, self.text_box, 2)

        # Initial positions
        x, y = self.text_box.x + 20, self.text_box.y + 20

        # --- Draw Quests ---
        y = self._draw_section(screen, "Quests", quests, completed_quests, x, y)

        # --- Draw Super Insults ---
        y = self._draw_section(screen, "Super Insults", super_insults, completed_super_insults, x, y, True)

        # --- Draw Insults ---
        self._draw_section(screen, "Insults", insults, completed_insults, x, y, True)

    def _draw_section(self, screen, header, text_list, completed_list, x, y, newline=False):
        if newline:
            y += self.spacing * 10  # Move y down for the list items
        # Render and blit the header
        header_surface = self.font.render(header, 1, pygame.Color('crimson'))
        screen.blit(header_surface, (x, y))
        y += header_surface.get_height() + self.spacing  # Move y down for the list items


        # Render and blit each list item with strikethrough if completed
        for text, completed in zip(text_list, completed_list):
            text_surface = self.font.render(text, 1, self.textcolor)
            if completed:
                pygame.draw.line(text_surface, self.textcolor, (0, text_surface.get_height() // 2), (text_surface.get_width(), text_surface.get_height() // 2), 2)
            screen.blit(text_surface, (x, y))
            y += text_surface.get_height() + self.spacing  # Move y down for the next item

        return y  # Return the updated y position for the next section

    def drawRng(self, screen, mood, quest, quest_difficulty, character_modifiers):
        # Render the bbox (same as before)
        screen.blit(self.bounding_box, self.text_box)
        pygame.draw.rect(screen, self.backgroundcolor, self.text_box, 2)

        # Draw rng scales
        scalesImage = pygame.image.load("assets/scales.png").convert_alpha()

        scalesImage = pygame.transform.scale(scalesImage, (128, 128))

        # Scales position
        x, y = self.text_box.x + 20, self.text_box.y + 20

        # Blit the icon
        # icon_x = x + num1_surface.get_width() + 10  # 10 pixels spacing
        screen.blit(scalesImage, (x, y))

        # # Initial positions
        # x, y = self.text_box.x + 20, self.text_box.y + 20

        # # Render number 1
        # num1_surface = self.font.render(str(mood), 1, self.textcolor)
        # screen.blit(num1_surface, (x, y))

    def drawMoods(self, screen, mood, mood_change):
        # Render the bbox (same as before)
        screen.blit(self.bounding_box, self.text_box)
        pygame.draw.rect(screen, self.backgroundcolor, self.text_box, 2)

        # Initial positions
        x, y = self.text_box.x + 20, self.text_box.y + 20

        # Render number 1
        num1_surface = self.font.render(str(mood), 1, self.textcolor)
        screen.blit(num1_surface, (x, y))

        if mood_change < 0:
            moodImage = pygame.image.load("assets/decrease.png").convert_alpha()
            mood_change = f'-{mood_change}'

        elif mood_change == 0:
            moodImage = pygame.image.load("assets/equal.png").convert_alpha()
            mood_change = f'{mood_change}'

        elif mood_change > 0:
            moodImage = pygame.image.load("assets/increase.png").convert_alpha()
            mood_change = f'+{mood_change}'

        moodImage = pygame.transform.scale(moodImage, (32, 32))

        # Blit the icon next to number 1
        icon_x = x + num1_surface.get_width() + 10  # 10 pixels spacing
        screen.blit(moodImage, (icon_x, y))

        # Render number 2 on a new line
        y += num1_surface.get_height() + self.spacing  # Move y down
        num2_surface = self.font.render(mood_change, 1, self.textcolor)
        screen.blit(num2_surface, (x + 20, y))