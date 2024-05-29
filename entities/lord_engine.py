import openai
import random


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

    def call_debug(self):
        mood=random.randint(-2,2)
        return {'mood':mood, 'quest':0}