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
        self.background_image = pygame.image.load("assets/main.jpg")
        self.background_image = pygame.transform.scale(self.background_image, self.game.resolution)
        self.background_rect = self.background_image.get_rect()

        self.start_button = UIButton(text="Start",
                                   width=self.game.resolution[0] // 4,
                                   height=self.game.resolution[1] // 10,
                                   pos=((self.game.resolution[0] - (self.game.resolution[0] // 4)) // 2,
                                        (self.game.resolution[1] - (self.game.resolution[1] // 10)) // 1.5),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.instructions_button = UIButton(text="Instructions",
                                   width=self.game.resolution[0] // 4,
                                   height=self.game.resolution[1] // 10,
                                   pos=((self.game.resolution[0] - (self.game.resolution[0] // 4)) // 2,
                                        (self.game.resolution[1] - (self.game.resolution[1] // 10)) // 1.25),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.quit_button = UIButton(text="Quit",
                                   width=self.game.resolution[0] // 4,
                                   height=self.game.resolution[1] // 10,
                                   pos=((self.game.resolution[0] - (self.game.resolution[0] // 4)) // 2,
                                        (self.game.resolution[1] - (self.game.resolution[1] // 10)) // 1.07),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.instructions_props = (self.game.resolution[0]//10, self.game.resolution[1] // 5,
                                8*self.game.resolution[0]//10, 6*self.game.resolution[1]//10)

        self.instructions_popup = UIPopupText(text=LOREM,
                                            fontsize=26,
                                            text_box_props = self.instructions_props,
                                            textcolor=(86, 54, 8),
                                            backgroundcolor=(255, 228, 157),
                                            margin=7,
                                            spacing=1)
        self.popup_on = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.start_button.clicked:
                self.game.change_state("live_play")
            elif self.instructions_button.clicked:
                self.popup_on = True
                try:
                    if self.instructions_popup.button.clicked:
                        self.popup_on= False
                        self.instructions_button.clicked= False
                        self.instructions_popup.button.clicked= False
                except AttributeError:
                    print('not initialized yet')

    def render(self):
        # Draw the background image
        self.game.screen.blit(self.background_image, self.background_rect)

        if self.popup_on:
            self.instructions_popup.draw(self.game.screen, True)

        else:
            # Draw the buttons
            self.start_button.draw_button(self.game.screen)
            self.instructions_button.draw_button(self.game.screen)
            self.quit_button.draw_button(self.game.screen)


        # Update the display
        pygame.display.flip()
