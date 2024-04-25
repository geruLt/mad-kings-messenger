import pygame
import sys

class MadKingsMessenger:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.resolution = (1280, 720)
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("Mad Kings Messenger")

        # Load the background image
        self.background_image = pygame.image.load("assets/throne_room_temp.jpg")
        self.background_image = pygame.transform.scale(self.background_image, self.resolution)
        self.background_rect = self.background_image.get_rect()

        # Set up the font
        self.font = pygame.font.Font(None, 32)

        # Set up the text input box
        self.text = ""
        self.input_box_props = (self.resolution[0]//10, 7 * self.resolution[1] // 8,
                                8*self.resolution[0]//10, self.resolution[1]//10)
        self.input_box = pygame.Rect(*self.input_box_props)

        # Set colors
        self.color_active = pygame.Color('dodgerblue1')
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_remaining_time = pygame.Color(255,165,0)
        self.color_consumed_time = pygame.Color('gray')
        self.color_text = pygame.Color('black')

        self.text_border_color = self.color_inactive
        self.active = False

        # Set up the bounding box
        self.bounding_box = pygame.Surface((self.input_box.width, self.input_box.height))
        self.bounding_box.set_alpha(128)
        self.bounding_box.fill((255, 255, 255))

        # Time variables for handling backspace key repetition and timer
        self.backspace_pressed = False

        self.backspace_timer = pygame.time.get_ticks()
        self.time_timer = pygame.time.get_ticks()

        self.backspace_interval = 50  # milliseconds
        self.time_interval = 1000  # milliseconds

        # Set up the health bar
        self.time_left = 100
        self.total_time = 100

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.text_border_color = self.color_active if self.active else self.color_inactive
            elif event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        # Here you can send the text to the background script
                        print("Text sent:", self.text)
                        self.text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace_pressed = True
                        self.backspace_timer = pygame.time.get_ticks()
                    else:
                        self.text += event.unicode
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_pressed = False

    def handle_backspace_repetition(self):
        if self.backspace_pressed:
            current_time = pygame.time.get_ticks()
            if current_time - self.backspace_timer > self.backspace_interval:
                self.backspace_timer = current_time
                if self.text:
                    self.text = self.text[:-1]

    def update_time_left(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_timer > self.time_interval:
            self.time_timer = current_time
            self.time_left -= 1

            # Update timeleft box
            self.timeleft_box_props = (self.resolution[0]//10,
                                        6.8 * self.resolution[1] // 8,
                                        int((8*self.resolution[0]//10) * (self.time_left/self.total_time)),
                                        self.resolution[1]//40)

            if self.time_left < 0:
                self.time_left = 0

    def render(self):
        # Draw the background image
        self.screen.blit(self.background_image, self.background_rect)

        # Draw the time bar background
        pygame.draw.rect(self.screen, self.color_consumed_time, (self.resolution[0]//10,
                                                                  6.8 * self.resolution[1] // 8,
                                                                  8*self.resolution[0]//10,
                                                                  self.resolution[1]//40))

        # Draw the remaining time bar
        pygame.draw.rect(self.screen, self.color_remaining_time, (self.resolution[0]//10,
                                                                   6.8 * self.resolution[1] // 8,
                                                                   int((8*self.resolution[0]//10) * (self.time_left/self.total_time)),
                                                                   self.resolution[1]//40))

        # Draw the input box and the text
        self.screen.blit(bounding_box, self.input_box)
        pygame.draw.rect(self.screen, self.text_border_color, self.input_box, 2)

        # Render the text
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.bounding_box.get_size()
        x, y = self.input_box_props[0], self.input_box_props[1]
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, self.color_text)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = self.input_box_props[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = self.input_box_props[0]  # Reset the x.
            y += word_height  # Start on new row.

        # Update the display
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.handle_backspace_repetition()
            self.update_time_left()
            self.render()
            clock.tick(30)