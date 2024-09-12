import itertools
import random

from otree.api import *
from os import environ
from openai import OpenAI
import json
import os
import requests

client = OpenAI(
  api_key=environ.get('OPENAI_API_KEY'),
)

author = 'Victor'
doc = """
Dennis-Victor Study
"""


class C(BaseConstants):
    NAME_IN_URL = 'dvstudy'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # chatGPT vars
    ## temperature (range 0 - 2)
    ## this sets the bot's creativity in responses, with higher values being more creative
    ## https://platform.openai.com/docs/api-reference/completions#completions/create-temperature
    TEMP = 1.2

    ## model
    ## this is which gpt model to use, which have different prices and ability
    ## https://platform.openai.com/docs/models
    MODEL = "GPT-4o"

    ## set character prompt. According to openAI's documentation, this should be less than ~1500 words
    CHARACTER_PROMPT_A = """ Never use any markdown or formatting in your answers."""

    #PEQ
    STANDARDCHOICESFIVE = [
        [1, 'Strongly agree'],
        [2, 'Agree'],
        [3, 'Neither agree nor disagree'],
        [4, 'Disagree'],
        [5, 'Strongly disagree'],
    ]
    STANDARDCHOICESTWO = [[0, "True"], [1, "False"]]
    STANDARDCHOICESTEN = [
        [0, '0 (Not at all)'],
        [1, '1'],
        [2, '2'],
        [3, '3'],
        [4, '4'],
        [5, '5'],
        [6, '6'],
        [7, '7'],
        [8, '8'],
        [9, '9'],
        [10, '10 (Very much)'],
    ]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    #instructions
    accept_instructions = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    Instr1 = models.IntegerField(
        choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect, blank=False
    )
    Instr2 = models.IntegerField(
        choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect, blank=False
    )
    Instr3 = models.IntegerField(
        choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect, blank=False
    )


    gen_check = models.IntegerField(blank=True, initial=0)
    save_image = models.BooleanField(blank=True, widget=widgets.CheckboxInput)
    surrogation = models.IntegerField()
    measure_skill = models.StringField()
    # avatar = models.StringField()
    seed = models.IntegerField(initial=0)
    url = models.StringField()

    #names
    main_name = models.StringField(blank=True)

    #features
    accessory = models.IntegerField(blank=True, label="Accessory")
    facial_hair = models.IntegerField(blank=True, label="Facial Hair")
    eye_sight = models.IntegerField(blank=True, label="Glasses")
    headgear = models.IntegerField(blank=True, label="Headgear")

    #chatgpt
    ai_condition = models.IntegerField(blank=True)
    chatLog = models.LongStringField(blank=True)
    # input data for gpt
    msg = models.LongStringField(blank=True)

    #PEQ - DEMOGRAPHICS
    # Demographics
    gender = models.IntegerField(
        label="Please select the gender you identify most with.",
        blank=False,
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other']
        ],
    )
    age = models.IntegerField(label="Please enter your age.", min=18, max=100, blank=False)
    education = models.IntegerField(
        label="What is the highest level of education that you have completed?",
        blank=False,
        choices=[
            [1, 'Less than High school'],
            [2, 'High school'],
            [3, 'College/University without undergraduate degree'],
            [4, 'Undergraduate (Bachelor, BSc, BA, etc.)'],
            [5, 'Graduate degree (Master, MS, MA, MSc, etc.)'],
            [6, 'Postgraduate (PhD, MBA, MD, etc.)'],
        ],
    )
    english = models.IntegerField(label="Please rate your English proficiency.", blank=False,
                                  choices=[
        [0, '0 (Very Poor)'],
        [1, '1'],
        [2, '2'],
        [3, '3'],
        [4, '4'],
        [5, '5'],
        [6, '6'],
        [7, '7'],
        [8, '8'],
        [9, '9'],
        [10, '10 (Excellent)']
    ])
    email = models.StringField(label="Please leave your email-address to receive the show-up fee and a chance to win one of the online shopping gift vouchers", blank=True)

    #PEQ - One
    ai_check = models.IntegerField(
        label="On the screen where I designed the character, I had access to a chatbox with ChatGPT at the top of the screen.",
        blank=False,
        choices=[
            [0, 'False'],
            [1, 'True'],
        ],
    )
    measure_check = models.IntegerField(
        label="This study measures whether each participant allocates points to 'Facial Hair.'",
        blank=False,
        choices=[
            [0, 'False'],
            [1, 'True'],
        ],
    )
    difficulty = models.IntegerField(
        label="How difficult was this study?",
        choices=[
            [1, 'Extremely easy'],
            [2, 'Moderately easy'],
            [3, 'Slightly easy'],
            [4, 'Neither easy nor difficult'],
            [5, 'Slightly difficult'],
            [6, 'Moderately difficult'],
            [7, 'Extremely difficult'],
        ],
        blank=False,
    )
    clarity = models.IntegerField(
        label="How clear were the instructions?",
        choices=[
            [1, 'Extremely clear'],
            [2, 'Moderately clear'],
            [3, 'Slightly clear'],
            [4, 'Neither clear nor unclear'],
            [5, 'Slightly unclear'],
            [6, 'Moderately unclear'],
            [7, 'Extremely unclear'],
        ],
        blank=False,
    )
    most_imp_attribute = models.IntegerField(
        label="Which attribute do you believe contributed most to creating an appealing and relatable character?",
        choices=[
            [1, 'Accessories'],
            [2, 'Facial Hair'],
            [3, 'Glasses'],
            [4, 'Head Gear'],
            [5, 'Each attribute contributed equally'],
        ],
        blank=False,
    )
    ai_usage = models.IntegerField(
        label="I use generative A.I., such as ChatGPT, regularly for work and studies.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )
    ai_helpful = models.IntegerField(
        label="Generative A.I., such as ChatGPT, is helpful for my work and studies.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )

    #PEQ - two
    creative_1 = models.IntegerField(
        label="I think I am a creative person.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )
    creative_2 = models.IntegerField(
        label="My creativity is important for who I am.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )
    creative_3 = models.IntegerField(
        label="Being a creative person is important to me.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )
    creative_4 = models.IntegerField(
        label="Creativity is an important part of myself.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )
    creative_5 = models.IntegerField(
        label="Ingenuity is a characteristic that is important to me.",
        blank=False,
        choices=C.STANDARDCHOICESFIVE
    )

# FUNCTIONS
def creating_session(subsession: Subsession):
    # randomize to treatments
    # Now always set to surrotation treatment
    treats = itertools.cycle([1, 2, 3])
    # skill_focus = itertools.cycle(['Accessory', 'Facial Hair', 'Glasses', 'Head Gear',])
    expConditions = itertools.cycle([1, 0])
    skill_focus = itertools.cycle(['Facial Hair'])
    for player in subsession.get_players():
        player.seed = random.randint(0, 999999)

        # if the config is measurement only
        if player.session.config['surrogation'] == 1:
            player.surrogation = player.session.config['surrogation']
            # randomize AI prompt and save to player var
            if player.session.config['ai_condition'] != "":
                player.ai_condition = player.session.config['ai_condition']
            else:
                player.ai_condition = next(expConditions)
                player.participant.vars['ai_condition'] = player.ai_condition
            print('set player.ai_condition to', player.ai_condition)

        # if the config is non-measurement only
        elif player.session.config['surrogation'] == 0:
            player.surrogation = player.session.config['surrogation']
            # randomize AI prompt and save to player var
            if player.session.config['ai_condition'] != "":
                player.ai_condition = player.session.config['ai_condition']
            else:
                player.ai_condition = 0
                player.participant.vars['ai_condition'] = player.ai_condition
            print('set player.ai_condition to', player.ai_condition)

        # randomize everything
        else:
            #determine treatment
            choose_treat = next(treats)
            if choose_treat == 1:
                player.surrogation = 0
                player.ai_condition = 0
            elif choose_treat == 2:
                player.surrogation = 1
                player.ai_condition = 0
            else:
                player.surrogation = 1
                player.ai_condition = 1
            # player.surrogation = next(treats)
            # # randomize AI prompt and save to player var
            # if player.surrogation == 1:
            #     if player.session.config['ai_condition'] != "":
            #         player.ai_condition = player.session.config['ai_condition']
            #     else:
            #         player.ai_condition = next(expConditions)
            #         player.participant.vars['ai_condition'] = player.ai_condition
            # elif player.surrogation == 0:
            #     player.ai_condition = 0
            #     player.participant.vars['ai_condition'] = player.ai_condition
            print('set player.ai_condition to', player.ai_condition)
            print('set player.surrogation to', player.surrogation)

        # set skill
        if player.surrogation == 1:
            player.measure_skill = next(skill_focus)
            print('set player.measure_skill to', player.measure_skill)

    # randomize avatar condition
    # Now always set to avatar treatment
    for player in subsession.get_players():
        # player.avatar = random.choice(['yes', 'no'])
        # player.avatar = 'yes'
        # print('set player.avatar to', player.avatar)

        # set prompt based on condition
        player.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_A}])



# custom export of chatLog
def custom_export(players):
    # header row
    yield ['session_code', 'participant_code', 'ai_condition', 'sender', 'text', 'timestamp']
    for p in players:
        participant = p.participant
        session = p.session

        # expand chatLog
        log = p.field_maybe_none('chatLog')
        if log:
            json_log = json.loads(log)
            print(json_log)
            for r in json_log:
                sndr = r['sender']
                txt = r['text']
                time = r['timestamp']
                yield [session.code, participant.code, p.ai_condition, sndr, txt, time]

# openAI chat gpt key
# CHATGPT_KEY = environ.get('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')

# function to run messages
def runGPT(inputMessage):
    try:
        completion = client.chat.completions.create(
            model = C.MODEL,
            messages = inputMessage,
            temperature = C.TEMP
        )

        response_content = completion.choices[0].message.content
        return response_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = ['accept_instructions']

    def error_message(player: Player, value):
        if value["accept_instructions"] != True:
            return 'You must accept the conditions to continue.'


class Introduction1(Page):
    form_model = 'player'
    form_fields = ['Instr1']

    def error_message(player: Player, value):
        if value["Instr1"] != 1:
            return 'Your answer is incorrect. You can win an online shopping gift voucher of 50 pounds depending on how well you perform on the task compared to others.'



class Introduction2(Page):
    form_model = 'player'
    form_fields = ['Instr2']

    def error_message(player: Player, value):
        if value["Instr2"] != 1:
            return 'Your answer is incorrect. Your task is to create a playable character that is as appealing and relatable as possible.'


class Introduction3(Page):
    form_model = 'player'
    form_fields = ['Instr3']

    def error_message(player: Player, value):
        if value["Instr3"] != 1:
            return 'Your answer is incorrect. Distributing the 100 points to the different attributes determines their importance for your character.'

class Introduction4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.ai_condition == 1

class Choice(Page):
    form_model = 'player'
    form_fields = [
        'accessory',
        'facial_hair',
        'eye_sight',
        'headgear',
        'chatLog',
        'main_name',
        'gen_check',
        'url',
        'save_image'
    ]

    @staticmethod
    def get_form_fields(player: Player):
        randomized_fields = [
            'accessory',
            'facial_hair',
            'eye_sight',
            'headgear'
        ]
        fixed_fields = [
            'chatLog',
            'main_name',
            'gen_check',
            'url',
            'save_image'
        ]
        random.shuffle(randomized_fields)  # Randomize the order of these fields
        return randomized_fields + fixed_fields  # Combine randomized and fixed fields

    @staticmethod
    def live_method(player: Player, data):

        # start GPT with prompt based on randomized ai_condition
        # set chatgpt api key
        #openai.api_key = CHATGPT_KEY
        client.api_key = environ.get('OPENAI_API_KEY')
        print('OpenAI key is', environ.get('OPENAI_API_KEY'))

        # load msg
        messages = json.loads(player.msg)

        # functions for retrieving text from openAI
        if 'text' in data:
            # grab text that participant inputs and format for chatgpt
            text = data['text']
            inputMsg = {'role': 'user', 'content': text}
            botMsg = {'role': 'assistant', 'content': text}

            # append messages and run chatgpt function
            messages.append(inputMsg)
            output = runGPT(messages)

            # also append messages with bot message
            botMsg = {'role': 'assistant', 'content': output}
            messages.append(botMsg)

            # write appended messages to database
            player.msg = json.dumps(messages)

            return {player.id_in_group: output}
        else:
            pass

    @staticmethod
    def before_next_page(player, timeout_happened):
        return {
        }

class Peq_intro(Page):
    pass

class Peq_one(Page):
    form_model = 'player'
    form_fields = [
        'ai_check',
        'measure_check',
        'difficulty',
        'clarity',
        'most_imp_attribute',
        'ai_helpful',
        'ai_usage'
    ]

    @staticmethod
    def get_form_fields(player: Player):
        fields = [
            'ai_check',
            'measure_check',
            'difficulty',
            'clarity',
            'most_imp_attribute',
            'ai_helpful',
            'ai_usage'
        ]
        random.shuffle(fields)
        return fields

class Peq_two(Page):
    form_model = 'player'
    form_fields = [
        'creative_1',
        'creative_2',
        'creative_3',
        'creative_4',
        'creative_5'
    ]

    @staticmethod
    def get_form_fields(player: Player):
        fields = [
            'creative_1',
            'creative_2',
            'creative_3',
            'creative_4',
            'creative_5'
        ]
        random.shuffle(fields)
        return fields

class Peq_demo(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'age',
        'english',
        'email'
    ]

class Final(Page):
    pass


page_sequence = [Welcome, Introduction1, Introduction2, Introduction3, Introduction4, Choice, Peq_intro, Peq_one, Peq_demo, Final]
