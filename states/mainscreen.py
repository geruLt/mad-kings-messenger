from .gamestate import GameState
from ui.button import UIButton
from ui.popup_text import UIPopupText

import sys
import pygame


LOREM = '''Welcome to the Mad Kings Messenger Demo!
This is a historical rpg game where you deliver messages for your king to other kingdoms as your mission as a messenger. You will use your own words to deliver the messages, so make sure to deliver them good. Your kingdom’s destiny is in your hands.
To play the game close this screen and press start demo, then you will be in the court of King Magnus of the Kingdom of Demetae. He is the ally of your kingdoms enemy Kingdom of Dumonii. You will need to convince him to change his side, or just stay neutral. You may also try to convince him to pay tribute to your kingdom’s war efforts. To play just select the text box on the bottom of the screen, type your message and press enter. You can see the effects of your messages on the right side of your text box. On top left you can track the quests and insults. You don’t have to insult the king but your own king will appreciate the humiliation of his enemies (and friends) so you will earn good money from them. On top of the text box you can see the time bar, make sure to say what you want before the timer ends!
'''

class MainScreen(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Load the background image
        self.background_image = pygame.image.load("assets/main.png")
        self.background_image = pygame.transform.scale(self.background_image, self.game.resolution)
        self.background_rect = self.background_image.get_rect()

        self.logoImage = pygame.image.load("assets/logo.png").convert_alpha()
        self.logoImage = pygame.transform.scale(self.logoImage, (670, 177))

        self.start_button = UIButton(text="New Game",
                                   width=400,
                                   height=90,
                                   pos=(600,540),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.load_button = UIButton(text="Load Game",
                                   width=400,
                                   height=90,
                                   pos=(600, 648),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.quit_button = UIButton(text="Quit",
                                   width=400,
                                   height=90,
                                   pos=(600, 756),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.load_popup = UIPopupText(text='Load Save File',
                                        on=False,
                                        quit_button=True,
                                        advance_button=False,
                                        fontsize=26,
                                        text_box_props = (160, 180, 1280, 540),
                                        textcolor=(86, 54, 8),
                                        backgroundcolor=(255, 228, 157, 200),
                                        margin=7,
                                        spacing=1)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.start_button.clicked:
                self.game.change_state("map")
            elif self.load_button.clicked:
                self.load_popup.on = True
                if self.load_popup.quit_button.clicked:
                    self.load_popup.on= False
                    self.load_button.clicked= False
                    self.load_popup.quit_button.clicked= False


    def render(self):
        # Draw the background image
        self.game.screen.blit(self.background_image, self.background_rect)

        # Draw the game logo
        self.game.screen.blit(self.logoImage, (50,50))

        if self.load_popup.on:
            self.load_popup.draw(self.game.screen)

        else:
            # Draw the buttons
            self.start_button.draw_button(self.game.screen)
            self.load_button.draw_button(self.game.screen)
            self.quit_button.draw_button(self.game.screen)


        # Update the display
        pygame.display.flip()
