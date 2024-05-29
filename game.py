from states import LivePlayState, MainScreen, MapState

import pygame

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
        # self.soundtrack.play(-1)

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


# Create the game
game = Game()

# Register the states
live_play_state = LivePlayState(game)
main_screen_state = MainScreen(game)
map_state = MapState(game)

game.register_state("live_play", live_play_state)
game.register_state("main_screen", main_screen_state)
game.register_state("map", map_state)

# Run the game
game.run()