import pygame
import sys
import openai

LOREM = '''Welcome to the Mad Kings Messenger Demo!
This is a historical rpg game where you deliver messages for your king to other kingdoms as your mission as a messenger. You will use your own words to deliver the messages, so make sure to deliver them good. Your kingdom’s destiny is in your hands.
To play the game close this screen and press start demo, then you will be in the court of King Magnus of the Kingdom of Demetae. He is the ally of your kingdoms enemy Kingdom of Dumonii. You will need to convince him to change his side, or just stay neutral. You may also try to convince him to pay tribute to your kingdom’s war efforts. To play just select the text box on the bottom of the screen, type your message and press enter. You can see the effects of your messages on the right side of your text box. On top left you can track the quests and insults. You don’t have to insult the king but your own king will appreciate the humiliation of his enemies (and friends) so you will earn good money from them. On top of the text box you can see the time bar, make sure to say what you want before the timer ends!
'''

SYSTEM_PROMPT = '''You are a game engine in an rpg game. You are the King of the Kingdom of Demetae. Your country is an ally of Kingdom of Dumonii, which is at war with Kingdom of Iceni. Your Kingdom has been neutral so far but Kingdom of Iceni is the strong side in this war. An emmisary from the Kingdom of Iceni just arrived, and is ready to deliver a message to you.

Depending on the situation, relations, and the delivered message return a mood score between -5 to +5 depending if this message made you angry or pleased.

Also there are a set of special messages you should check for, these are quests. If any of these quest messages are delivered to you, state it in a special form.

quests = ['Break the allience with Dumonii Kingdom',
                      'Yearly tribute of 500 golds',
                      'Assist our kingdom in war with Dumonii Kingdom']

For example, if the player gives you this message:

"Greetings Lord Magnus, my great King is not pleased that you are still a friend to the evil Dumonii Kingdom, he wants you to break the alliance at once or else!'

You should get mad, but notice one of the quests are complete since the player asked you to 'Break the allience with Dumonii Kingdom'. So you should give an answer in this special json format, with mood and done quest index:
{'mood'=-4, 'quest'=0}

If no quest was done in the message and it was a message that praised you, you would return:
{'mood'=3, 'quest'=None}'''

# Define the base class for game states
class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


class LivePlayState(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Load the game AI engine
        self.lord_engine = LordEngine()

        # Load the background image
        self.background_image = pygame.image.load("assets/throne_room_temp.jpg")
        self.background_image = pygame.transform.scale(self.background_image, self.game.resolution)
        self.background_rect = self.background_image.get_rect()

        # Set up the text input box
        self.user_input = ""
        self.quest = ['Break the allience with Dumonii Kingdom',
                      'Yearly tribute of 500 golds',
                      'Assist our kingdom in war with Dumonii Kingdom']

        self.super_insults = ['Your Baldness', 'King Shine-a-Lot']
        self.insults = ['Smooth',  'Glowing', 'Polished']

        self.completed_quests = [False, False, False]
        self.completed_super_insults = [False, False]
        self.completed_insults = [False, False, False]

        self.input_box_props = (self.game.resolution[0] // 10, 6.6 * self.game.resolution[1] // 8,
                                8 * self.game.resolution[0] // 10, self.game.resolution[1] // 7)

        self.input_box = PopupText(text = self.user_input,
                                   fontsize = 24,
                                   text_box_props= self.input_box_props,
                                   textcolor=(86, 54, 8),
                                   backgroundcolor=(255, 228, 157),
                                   margin=7,
                                   spacing=1)

        self.quest_box_props = (0.1*self.game.resolution[0] // 10, 1*self.game.resolution[1] // 8,
                                3.5*self.game.resolution[0] // 10, 3.5*self.game.resolution[1] // 8)

        self.quest_box = PopupText(text = '',
                                   fontsize = 24,
                                   text_box_props= self.quest_box_props,
                                   textcolor=(86, 54, 8),
                                   backgroundcolor=(255, 228, 157),
                                   margin=7,
                                   spacing=1)

        self.mood_box_props = (9.1*self.game.resolution[0] // 10, 6.7 * self.game.resolution[1] // 8,
                                1*self.game.resolution[0] // 16, 1*self.game.resolution[1] // 9)

        self.mood_box = PopupText(text = '',
                                   fontsize = 24,
                                   text_box_props= self.mood_box_props,
                                   textcolor=(86, 54, 8),
                                   backgroundcolor=(255, 228, 157),
                                   margin=7,
                                   spacing=1)


        self.results_box_props = (2.5*self.game.resolution[0]//10, self.game.resolution[1] // 5,
                                5*self.game.resolution[0]//10, 4*self.game.resolution[1]//10)

        self.results_box = PopupText(text='',
                                     fontsize=26,
                                     text_box_props = self.results_box_props,
                                     textcolor=(86, 54, 8),
                                     backgroundcolor=(255, 228, 157),
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
        self.update_time_left()

    def evaluate_message(self):
        # Reset the mood change
        self.mood_change = 0

        # Call the engine
        output = self.lord_engine.call(self.user_input)

        # Update the moods
        self.mood_change += int(output['mood'])

        if output['quest'] != None:
            self.completed_quests[int(output['quest'])] = True

        for idx, insult in enumerate(self.super_insults):
            if insult in self.user_input:
                self.completed_super_insults[idx] = True
                self.mood_change -= 5

        for idx, insult in enumerate(self.insults):
            if insult in self.user_input:
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
Total Quests Done: {sum(self.completed_quests)}
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

        else:
            self.results_box.draw(self.game.screen, offset= 0.5* self.game.resolution[0] // 10)


        # Update the display
        pygame.display.flip()


class MainScreen(GameState):
    def __init__(self, game):
        super().__init__(game)

        # Load the background image
        self.background_image = pygame.image.load("assets/main.jpg")
        self.background_image = pygame.transform.scale(self.background_image, self.game.resolution)
        self.background_rect = self.background_image.get_rect()

        self.start_button = Button(text="Start",
                                   width=self.game.resolution[0] // 4,
                                   height=self.game.resolution[1] // 10,
                                   pos=((self.game.resolution[0] - (self.game.resolution[0] // 4)) // 2,
                                        (self.game.resolution[1] - (self.game.resolution[1] // 10)) // 1.5),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.instructions_button = Button(text="Instructions",
                                   width=self.game.resolution[0] // 4,
                                   height=self.game.resolution[1] // 10,
                                   pos=((self.game.resolution[0] - (self.game.resolution[0] // 4)) // 2,
                                        (self.game.resolution[1] - (self.game.resolution[1] // 10)) // 1.25),
                                   elevation=10,
                                   color = (128, 128, 128, 128),
                                   shadow=  (100, 100, 100, 128),
                                   hover=  (200, 200, 200, 128))

        self.instructions_props = (self.game.resolution[0]//10, self.game.resolution[1] // 5,
                                8*self.game.resolution[0]//10, 6*self.game.resolution[1]//10)

        self.instructions_popup = PopupText(text=LOREM,
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

        # Update the display
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.resolution = (1600, 900)
        self.screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.states = {}
        self.current_state = None
        pygame.mixer.init()
        self.soundtrack = pygame.mixer.Sound('assets/soundtrack.ogg')
        self.soundtrack.play(-1)


    def register_state(self, state_name, state):
        self.states[state_name] = state

    def change_state(self, state_name):
        if state_name in self.states:
            self.current_state = self.states[state_name]

    def run(self):
        self.change_state("main_screen")

        while True:
            self.current_state.handle_events()
            self.current_state.update()
            self.current_state.render()
            self.clock.tick(30)


class Button():
    def __init__(self, text, width, height, pos, elevation, color, shadow, hover):
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
        font = pygame.font.SysFont('rockwell', 50)
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

class PopupText:
    def __init__(self, text, fontsize, text_box_props, textcolor, backgroundcolor, margin, spacing):
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
            self.button = Button(text="x",
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

class LordEngine:
    def __init__(self):
        self.client = openai.OpenAI(
            base_url = "https://api.endpoints.anyscale.com/v1",
            api_key = "esecret_necfgmmwhuz99bc7hi4cpbyrr3"
        )

        self.model = "mlabonne/NeuralHermes-2.5-Mistral-7B"
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.temperature = 1

    def update_messages(self, role, content):
        self.messages.append({"role": role, "content": content})

    def call(self, text):
        self.update_messages('user', text)

        chat_completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature
        )

        output = chat_completion.choices[0].message.content
        start_index = output.find("{")
        end_index = output.rfind("}") + 1
        output_fixed = output[start_index:end_index]

        self.update_messages('assistant', output_fixed)
        print(output_fixed)
        return eval(output_fixed)


# Create the game
game = Game()

# Register the states
live_play_state = LivePlayState(game)
main_screen_state = MainScreen(game)

game.register_state("live_play", live_play_state)
game.register_state("main_screen", main_screen_state)

# Run the game
game.run()