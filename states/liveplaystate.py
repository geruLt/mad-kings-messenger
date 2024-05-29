from .gamestate import GameState
from entities import LordEngine
from ui.button import UIButton
from ui.popup_text import UIPopupText

import sys
import pygame
import random

class LivePlayState(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Load the game AI engine
        self.lord_engine = LordEngine()

        # Load the background image
        self.background_image = pygame.image.load("assets/throne_room_temp.jpg")
        self.background_image = pygame.transform.scale(self.background_image, self.game.resolution)
        self.background_rect = self.background_image.get_rect()

        self.scalesImage = pygame.image.load("assets/scales.png").convert_alpha()
        self.scalesImage = pygame.transform.scale(self.scalesImage, (256, 256))

        # Set up the text input box
        self.user_input = ""
        self.quest = ["Sign a non-agression pact",
                        "Pay a yearly tribute of 500 golds",
                        "Join our kingdom in war with Gemeshmian Empire"]
        self.quest_diff = [12, 16, 20]

        self.super_insults = ['Your Baldness']
        self.insults = ['Smooth',  'Glowing', 'Polished']

        self.completed_quests = [False, False, False]
        self.quest_sucess = [False, False, False]
        self.completed_super_insults = [False, False]
        self.completed_insults = [False, False, False]

        self.input_box = UIPopupText(text = self.user_input,
                                   on = True,
                                   quit_button=False,
                                   advance_button=False,
                                   fontsize = 24,
                                   text_box_props= (160, 740, 1280, 130),
                                   textcolor=(86, 54, 8),
                                   backgroundcolor=(255, 228, 157, 200),
                                   margin=7,
                                   spacing=1)

        self.quest_box = UIPopupText(text = '',
                                   on = True,
                                   quit_button=False,
                                   advance_button=False,
                                   fontsize = 24,
                                   text_box_props= (20, 110, 560, 390),
                                   textcolor=(86, 54, 8),
                                   backgroundcolor=(255, 228, 157, 200),
                                   margin=7,
                                   spacing=1)

        self.mood_box = UIPopupText(text = '',
                                   on = True,
                                   quit_button=False,
                                   advance_button=False,
                                   fontsize = 24,
                                   text_box_props= (1460, 750, 100, 100),
                                   textcolor=(86, 54, 8),
                                   backgroundcolor=(255, 228, 157, 200),
                                   margin=7,
                                   spacing=1)

        self.rng_visual_popup = UIPopupText(text='',
                                            on = False,
                                            quit_button=True,
                                            advance_button=True,
                                            fontsize=26,
                                            text_box_props =(160, 180, 1280, 540),
                                            textcolor=(86, 54, 8),
                                            backgroundcolor=(255, 228, 157, 255),
                                            margin=7,
                                            spacing=1)

        self.results_box = UIPopupText(text='',
                                     on = False,
                                     quit_button=False,
                                     advance_button=True,
                                     fontsize=26,
                                     text_box_props = (400, 180, 320, 360),
                                     textcolor=(86, 54, 8),
                                     backgroundcolor=(255, 228, 157, 255),
                                     margin=7,
                                     spacing=1)


        # Set up the colors
        self.color_remaining_time = pygame.Color(255, 165, 0)
        self.color_consumed_time = pygame.Color('gray')

        # Set up boolean state trackers
        self.input_active = False
        self.backspace_pressed = False
        self.game_over = False

        # Set the timers
        self.backspace_timer = pygame.time.get_ticks()
        self.time_timer = pygame.time.get_ticks()
        self.pause = False

        # Set constants
        self.BACKSPACE_INTERVAL = 50  # milliseconds
        self.TIME_INTERVAL = 1000  # milliseconds

        # Set game mechanic variables
        self.time_left = 180
        self.total_time = 180
        self.mood = 50
        self.mood_change = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.text_box.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        # Here you can send the text to the background script
                        print("Text sent:", self.user_input)
                        self.evaluate_message()
                        self.user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks()
                    else:
                        self.user_input += event.unicode
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = False

        self.handle_backspace_repetition()

        if not self.pause:
            self.update_time_left()

        if self.rng_visual_popup.quit_button.clicked:
            self.rng_visual_popup.on= False
            self.rng_visual_popup.quit_button.clicked= False
            self.pause = False
        elif self.rng_visual_popup.advance_button.clicked:
            self.rng_visual_popup.on= False
            self.rng_visual_popup.advance_button.clicked= False
            self.pause = False

    def evaluate_message(self):
        # Reset the mood change
        self.mood_change = 0

        # Call the engine
        output = self.lord_engine.call(self.user_input)
        # output = self.lord_engine.call_debug()

        # Update the moods
        self.mood_change += int(output['mood'])

        if output['quest'] != None:
            self.completed_quests[int(output['quest'])] = True
            self.pause = True
            chance = (20 - self.quest_diff[int(output['quest'])])* 5
            quest_success = (random.random() * 100) < chance
            _success = 'Success' if quest_success else 'Fail'
            text = f"\n\n\n\n\n\n\n\n\n\n\nQuest Completion\nQuest: {self.quest[int(output['quest'])]}\nChance:{chance}% >>> {_success}"
            self.rng_visual_popup.text = text
            self.rng_visual_popup.on = True

        for idx, insult in enumerate(self.super_insults):
            if insult.lower() in self.user_input.lower():
                self.completed_super_insults[idx] = True
                self.mood_change -= 5

        for idx, insult in enumerate(self.insults):
            if insult.lower() in self.user_input.lower():
                self.completed_insults[idx] = True
                self.mood_change -= 3

        self.mood += self.mood_change

        if self.mood <= 0:
            self.game_over = True

    def handle_backspace_repetition(self):
        if self.backspace_pressed:
            current_time = pygame.time.get_ticks()
            if current_time - self.backspace_timer > self.BACKSPACE_INTERVAL:
                self.backspace_timer = current_time
                if self.user_input:
                    self.user_input = self.user_input[:-1]

    def update_time_left(self):
        current_time = pygame.time.get_ticks()
        self.time_left -= (current_time - self.time_timer)/1000
        self.time_timer = current_time

        if self.time_left <= 0:
           self.get_results()
           self.game_over = True

    def get_results(self):
        end_text = f'''
Game Over
Total Quests Done: {sum(self.quest_sucess)}
Total Super Insults: {sum(self.completed_super_insults)}
Total Insults: {sum(self.completed_insults)}
Final Lord Mood: {self.mood}
    '''
        self.results_box.text = end_text

    def render(self):
        # Draw the background image
        self.game.screen.blit(self.background_image, self.background_rect)

        if not self.game_over:
            # Draw the time bar background
            pygame.draw.rect(self.game.screen, self.color_consumed_time, (self.game.resolution[0] // 10,
                                                                        6.4 * self.game.resolution[1] // 8,
                                                                        8 * self.game.resolution[0] // 10,
                                                                        self.game.resolution[1] // 40))

            # Draw the remaining time bar
            pygame.draw.rect(self.game.screen, self.color_remaining_time, (self.game.resolution[0] // 10,
                                                                            6.4 * self.game.resolution[1] // 8,
                                                                            int((8 * self.game.resolution[0] // 10) * (self.time_left / self.total_time)),
                                                                            self.game.resolution[1] // 40))

            # Draw the text boxes
            self.input_box.text = self.user_input
            self.input_box.draw(self.game.screen, False, self.input_active)

            self.quest_box.drawQuests(self.game.screen, self.quest, self.super_insults, self.insults,
                                    self.completed_quests, self.completed_super_insults, self.completed_insults)

            self.mood_box.drawMoods(self.game.screen, self.mood, self.mood_change)

            if self.rng_visual_popup.on:
                self.rng_visual_popup.draw(self.game.screen)
                self.game.screen.blit(self.scalesImage, (672, 210))


        else:
            self.results_box.draw(self.game.screen, offset= 0.5* self.game.resolution[0] // 10)


        # Update the display
        pygame.display.flip()