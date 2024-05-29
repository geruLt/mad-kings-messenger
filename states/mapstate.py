from .gamestate import GameState
from ui import UIButton
from ui import UIPopupText
from entities import Country, Observer

import sys
import pygame


class MapState(GameState):
    '''Overalview state of the game.'''
    def __init__(self, game):
        super().__init__(game)

        # Load the background image
        self.background_image = pygame.image.load("assets/worldmap.png")
        self.background_image = pygame.transform.scale(self.background_image, self.game.resolution)
        self.background_rect = self.background_image.get_rect()

        self.relationships_button = UIButton(text="Diplomacy",
                                   width=140,
                                   height=45,
                                   pos=(50,50),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128),
                                   fontsize= 25)

        self.relationships_popup = UIPopupText(text='Diplomacy Placeholder',
                                    on= False,
                                    quit_button=True,
                                    advance_button=False,
                                    fontsize=26,
                                    text_box_props = (160, 180, 1280, 540),
                                    textcolor=(86, 54, 8),
                                    backgroundcolor=(255, 228, 157,220),
                                    margin=7,
                                    spacing=1)

        self.strengths_button = UIButton(text="Power",
                                   width=100,
                                   height=45,
                                   pos=(200, 50),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128),
                                   fontsize= 25)

        self.strengths_popup = UIPopupText(text='Power Placeholder',
                                    on= False,
                                    quit_button=True,
                                    advance_button=False,
                                    fontsize=26,
                                    text_box_props = (160, 180, 1280, 540),
                                    textcolor=(86, 54, 8),
                                    backgroundcolor=(255, 228, 157, 220),
                                    margin=7,
                                    spacing=1)

        self.logs_button = UIButton(text="Logs",
                                   width=90,
                                   height=45,
                                   pos=(310, 50),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128),
                                   fontsize= 25)

        self.logs_popup = UIPopupText(text='Logs Placeholder',
                                    on= False,
                                    quit_button=True,
                                    advance_button=False,
                                    fontsize=26,
                                    text_box_props = (160, 180, 1280, 540),
                                    textcolor=(86, 54, 8),
                                    backgroundcolor=(255, 228, 157, 220),
                                    margin=7,
                                    spacing=1)

        self.shop_button = UIButton(text="Shop",
                                   width=90,
                                   height=45,
                                   pos=(410, 50),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128),
                                   fontsize= 25)

        self.shop_popup = UIPopupText(text='Shop Placeholder',
                                    on= False,
                                    quit_button=True,
                                    advance_button=False,
                                    fontsize=26,
                                    text_box_props = (160, 180, 1280, 540),
                                    textcolor=(86, 54, 8),
                                    backgroundcolor=(255, 228, 157, 220),
                                    margin=7,
                                    spacing=1)

        self.buy_button = UIButton(text="+",
                                   width=35,
                                   height=35,
                                   pos=(670, 315),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128),
                                   fontsize= 25)

        self.quest_button = UIButton(text="To Mission",
                                   width=130,
                                   height=45,
                                   pos=(1350, 800),
                                   elevation=10,
                                   color = (255, 100, 100, 160),
                                   shadow=  (255, 100, 100, 160),
                                   hover=  (255, 50, 50, 160),
                                   fontsize= 25)

        self.quest_popup = UIPopupText(text='Mission Placeholder',
                                    on= False,
                                    quit_button=True,
                                    advance_button=True,
                                    fontsize=26,
                                    text_box_props = (160, 180, 1280, 540),
                                    textcolor=(86, 54, 8),
                                    backgroundcolor=(255, 228, 157, 220),
                                    margin=7,
                                    spacing=1)

        self.countries = self._init_countries()
        self.observer = Observer(countries=self.countries)

    def _init_countries(self):
        countries = []

        # Define story country information
        country_names = ['Kingdom of Uria',
                         'Grand Duchy of Corducia',
                         'Kingdom of Kroberle',
                         'Gemeshmian Empire',
                         'Calen']

        ruler_names = ['King Reynfrey',
                       'Grand Duke Ingelram',
                       'King Balian',
                       'Emperor Blavier',
                       'General Rauffe']

        strengths = [700, 550, 500, 900, 600]

        relationships = [100, 80, 50, 10, 35]

        statuses = ['Self', 'Ally', 'Neutral', 'War', 'Tension']

        positions = [(None, None),
                     (390, 470),
                     (570, 390),
                     (970, 470),
                     (1170, 580)]

        # Set the countries
        for country, ruler, strength, relationship, status, position in zip(country_names,
                                                                  ruler_names,
                                                                  strengths,
                                                                  relationships,
                                                                  statuses,
                                                                  positions):
            countries.append(Country(name=country,
                                     ruler_name=ruler,
                                     strength=strength,
                                     relationship=relationship,
                                     status=status,
                                     position=position))

        return countries

    def _draw_icons(self):
        for country in self.countries:
            if country.status == 'Ally':
                stateImage = pygame.image.load("assets/ally.png").convert_alpha()
                stateImage = pygame.transform.scale(stateImage, (64, 64))
                self.game.screen.blit(stateImage, country.position)
            elif country.status == 'Neutral':
                stateImage = pygame.image.load("assets/neutral.png").convert_alpha()
                stateImage = pygame.transform.scale(stateImage, (64, 64))
                self.game.screen.blit(stateImage, country.position)
            elif country.status == 'Tension':
                stateImage = pygame.image.load("assets/tension.png").convert_alpha()
                stateImage = pygame.transform.scale(stateImage, (64, 64))
                self.game.screen.blit(stateImage, country.position)
            elif country.status == 'War':
                stateImage = pygame.image.load("assets/war.png").convert_alpha()
                stateImage = pygame.transform.scale(stateImage, (64, 64))
                self.game.screen.blit(stateImage, country.position)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif self.relationships_button.clicked:
                # Open the target popup
                self._update_relationships()
                self.relationships_popup.on = True
                # If the popup is closed
                if self.relationships_popup.quit_button.clicked:
                    self.relationships_popup.on= False
                    self.relationships_button.clicked= False
                    self.relationships_popup.quit_button.clicked= False

            elif self.strengths_button.clicked:
                # Open the target popup
                self._update_strengths()
                self.strengths_popup.on = True
                # If the popup is closed
                if self.strengths_popup.quit_button.clicked:
                    self.strengths_popup.on= False
                    self.strengths_button.clicked= False
                    self.strengths_popup.quit_button.clicked= False

            elif self.logs_button.clicked:
                # Open the target popup
                self._update_logs()
                self.logs_popup.on = True
                # If the popup is closed
                if self.logs_popup.quit_button.clicked:
                    self.logs_popup.on= False
                    self.logs_button.clicked= False
                    self.logs_popup.quit_button.clicked= False

            elif self.shop_button.clicked:
                # Open the target popup
                self._update_shop()
                self.shop_popup.on = True
                # If the popup is closed
                if self.shop_popup.quit_button.clicked:
                    self.shop_popup.on= False
                    self.shop_button.clicked= False
                    self.shop_popup.quit_button.clicked= False
            if self.buy_button.clicked:
                if self.observer.money >= 100:
                    self.observer.money -= 100
                    self.observer.gifts += 1
                self.buy_button.clicked = False

            elif self.quest_button.clicked:
                # Open the target popup
                self._update_quests()
                self.quest_popup.on = True
                # If the popup is closed
                if self.quest_popup.quit_button.clicked:
                    self.quest_popup.on= False
                    self.quest_button.clicked= False
                    self.quest_popup.quit_button.clicked= False
                if self.quest_popup.advance_button.clicked:
                    self.game.states['live_play'].backspace_timer = pygame.time.get_ticks()
                    self.game.states['live_play'].time_timer = pygame.time.get_ticks()
                    self.game.change_state("live_play")

    def _update_relationships(self):
        text = 'Diplomacy \n\n'
        # Fill text with country diplomacy stats
        for country in self.countries:
            if country.status != 'Self':
                _text = f'{country.name}: {country.status} ({country.relationship})\n'
                text += _text

        # Update the popup text
        self.relationships_popup.text = text

    def _update_strengths(self):
        text = 'Power \n\n'
        # Fill text with country diplomacy stats
        for country in self.countries:
            _text = f'{country.name}: {country.strength} ({country.status})\n'
            text += _text

        # Update the popup text
        self.strengths_popup.text = text

    def _update_logs(self):
        text = 'Logs\nWinter 1165: Gemeshmian Empire declared war on Kingdom of Uria'
        self.logs_popup.text = text

    def _update_shop(self):
        text = f'Shop\nTotal Gold:{self.observer.money}\n'
        text += f'Genereous Gift <extends time>: 100 Gold ({self.observer.gifts})'
        self.shop_popup.text = text

    def _update_quests(self):
        text = self.observer.get_mission_details()
        self.quest_popup.text = text

    def render(self):
        # Draw the background image
        self.game.screen.blit(self.background_image, self.background_rect)

        # Draw the state icons
        self._draw_icons()

        # Check if any popups are on if so draw them
        if self.relationships_popup.on:
            self.relationships_popup.draw(self.game.screen)
        elif self.strengths_popup.on:
            self.strengths_popup.draw(self.game.screen)
        elif self.logs_popup.on:
            self.logs_popup.draw(self.game.screen)
        elif self.shop_popup.on:
            self.shop_popup.draw(self.game.screen)
            self.buy_button.draw_button(self.game.screen)
        elif self.quest_popup.on:
            self.quest_popup.draw(self.game.screen)
        else:
            # Draw the buttons
            self.relationships_button.draw_button(self.game.screen)
            self.strengths_button.draw_button(self.game.screen)
            self.logs_button.draw_button(self.game.screen)
            self.shop_button.draw_button(self.game.screen)
            self.quest_button.draw_button(self.game.screen)

        # Update the display
        pygame.display.flip()