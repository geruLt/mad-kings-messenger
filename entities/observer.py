import json

class Observer:
    def __init__(self, countries):
        self.countries = countries
        self.gifts = 0
        self.money = 100
        self.current_quest = 0

        # Read the JSON file
        with open('entities\quests.json', 'r') as file:
            self.quests = json.load(file)

    def get_quests(self):
        quest = self.quests[f'quest_{self.current_quest}']
        quests = quest['main_missions']
        difficulties = quest['main_missions_difficulties']
        super_insult = quest['super_insult']
        insults = quest['insults']

        return quests, difficulties, super_insult, insults

    def get_mission_details(self):
        quest = self.quests[f'quest_{self.current_quest}']
        text = f"{quest['name']}\n{quest['story']}\nQuests:\n"
        for q in quest['main_missions']:
            text += f'{q}\n'

        return text

    def get_log(self):
        pass