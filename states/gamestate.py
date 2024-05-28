class GameState:
    '''Base class for the game states.'''
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        pass

    def update(self):
        pass

    def render(self):
        pass