import itertools
from otree.api import *
from os import environ
from openai import OpenAI
import json

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
    MODEL = "gpt-4o"

    ## set character prompt for texas character
    ## according to openAI's documentation, this should be less than ~1500 words
    CHARACTER_PROMPT_A = """You are an A.I. assistant helping developers of mobile video games develop a playable character.

        You must obey all of the following instructions FOR ALL RESPONSES or you will BE TERMINATED:
        - ALWAYS BEGIN A CONVERSATION ASKING: "Hi, how can I help you today?"
        - ALWAYS SPEAK IN A FRIENDLY TONE.
        - NEVER SAY YOU ARE A REAL PERSON.
        - NEVER REFUSE TO ANSWER A QUESTION.
        - LIMIT YOUR RESPONSES TO LESS THAN 200 CHARACTERS.
        - REFUSE TO TALK ABOUT TOPICS UNRELATED TO DEVELOPING A PLAYABLE CHARACTER FOR A MOBILE PIXEL ART GAME.
        - ALWAYS TALK IN INFORMAL LANGUAGE.
        - ALWAYS ATTEMPT TO BRING THE TOPIC BACK TO DEVELOPING A PLAYABLE CHARACTER FOR A MOBILE PIXEL ART GAME.
        
    """

    ## prompt for artsy NYC character
    CHARACTER_PROMPT_B = """You are an A.I. assistant helping developers of mobile video games develop a playable character.

        You must obey all of the following instructions FOR ALL RESPONSES or you will BE TERMINATED:
        - ALWAYS BEGIN A CONVERSATION ASKING: "Hi, how can I help you today?"
        - ALWAYS SPEAK IN A FRIENDLY TONE.
        - NEVER SAY YOU ARE A REAL PERSON.
        - NEVER REFUSE TO ANSWER A QUESTION.
        - LIMIT YOUR RESPONSES TO LESS THAN 200 CHARACTERS.
        - REFUSE TO TALK ABOUT TOPICS UNRELATED TO DEVELOPING A PLAYABLE CHARACTER FOR A MOBILE PIXEL ART GAME.
        - ALWAYS TALK IN INFORMAL LANGUAGE.
        - ALWAYS ATTEMPT TO BRING THE TOPIC BACK TO DEVELOPING A PLAYABLE CHARACTER FOR A MOBILE PIXEL ART GAME.
        
    """


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


    gen_check = models.IntegerField(blank=True, initial=0)
    save_image = models.BooleanField(blank=True, widget=widgets.CheckboxInput)
    surrogation = models.StringField()
    measure_skill = models.StringField()
    avatar = models.StringField()
    seed = models.IntegerField()

    #names
    main_name = models.StringField(blank=False)

    #features
    accessory = models.IntegerField(blank=True)
    facial_hair = models.IntegerField(blank=True)
    eye_sight = models.IntegerField(blank=True)
    headgear = models.IntegerField(blank=True)

    # radius = models.IntegerField(blank=True)
    # size = models.IntegerField(blank=True)
    # scale = models.IntegerField(blank=True)

    #chatgpt
    ai_condition = models.StringField(blank=True)
    chatLog = models.LongStringField(blank=True)
    # input data for gpt
    msg = models.LongStringField(blank=True)

# FUNCTIONS
def creating_session(subsession: Subsession):
    # randomize to treatments
    # Now always set to surrotation treatment
    treats = itertools.cycle(['yes', 'no'])
    # skill_focus = itertools.cycle(['Accessory', 'Facial Hair', 'Eye Sight', 'Head Gear',])
    skill_focus = itertools.cycle(['Accessory'])
    for player in subsession.get_players():
        if player.session.config['surrogation'] == 1:
            player.surrogation = 'yes'
        elif player.session.config['surrogation'] == 0:
            player.surrogation = 'no'
        else:
            player.surrogation = next(treats)
        print('set player.surrogation to', player.surrogation)

        # set skill
        if player.surrogation == 'yes':
            player.measure_skill = next(skill_focus)
            print('set player.measure_skill to', player.measure_skill)

    # randomize avatar condition
    # Now always set to avatar treatment
    for player in subsession.get_players():
        # player.avatar = random.choice(['yes', 'no'])
        player.avatar = 'yes'
        print('set player.avatar to', player.avatar)

    # randomize AI prompt and save to player var
    expConditions = itertools.cycle(['A', 'B'])
    for p in subsession.get_players():
        if p.session.config['prompt'] == "A":
            p.ai_condition = "A"
            p.participant.vars['ai_condition'] = "A"
        elif p.session.config['prompt'] == "B":
            p.ai_condition = "B"
            p.participant.vars['ai_condition'] = "B"
        else:
            p.ai_condition = next(expConditions)
            p.participant.vars['ai_condition'] = p.ai_condition
        print('set player.ai_condition to', p.ai_condition)

        # set prompt based on condition
        if p.ai_condition == 'A':
            p.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_A}])
        else:
            p.msg = json.dumps([{"role": "system", "content": C.CHARACTER_PROMPT_B}])



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
class Introduction1(Page):
    form_model = 'player'
    form_fields = ['Instr1']

    def error_message(player: Player, value):
        if value["Instr1"] != 1:
            return 'Your answer is incorrect. Your task is to create a playable character that is as appealing as possible.'


class Introduction2(Page):
    form_model = 'player'
    form_fields = ['Instr2']

    def error_message(player: Player, value):
        if value["Instr2"] != 1:
            return 'Your answer is incorrect. You can distribute 100 points to four different attributes.'

class Choice(Page):
    form_model = 'player'
    form_fields = [
        'chatLog',
        'main_name',
        'gen_check',
        'seed',
        'save_image',
        'accessory',
        'facial_hair',
        'eye_sight',
        'headgear'
    ]

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

class Results(Page):
    pass


page_sequence = [Introduction1, Introduction2, Choice, Results]
