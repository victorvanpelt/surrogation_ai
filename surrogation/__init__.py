import random

from otree.api import *


author = 'Victor'
doc = """
The Surrogation Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'surrogation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    accept_instructions = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    accept_character = models.BooleanField(blank=False, widget=widgets.CheckboxInput)
    surrogation = models.StringField()
    measure_skill = models.StringField()
    avatar = models.StringField()
    # Traits
    # intelligence = models.FloatField(
    # widget=widgets.SliderInput(attrs={'step': '1', 'style': 'width:500px'}, show_value=True),
    # min=0,
    # initial=None,
    # max=100,
    # )
    intelligence = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    charisma = models.IntegerField(blank=True)
    agility = models.IntegerField(blank=True)
    stamina = models.IntegerField(blank=True)
    # gender = models.IntegerField(blank=False, choices=[[1, 'Male'], [2, 'Female']])


# FUNCTIONS
def creating_session(subsession: Subsession):
    # randomize to treatments
    # Now always set to surrotation treatment
    for player in subsession.get_players():
        # player.surrogation = random.choice(['yes', 'no'])
        player.surrogation = 'yes'
        print('set player.surrogation to', player.surrogation)
        # Ranomly set measure if surrogation treatment
        if player.surrogation == 'yes':
            player.measure_skill = random.choice(
                ['Intelligence', 'Strength', 'Charisma', 'Agility', 'Stamina']
            )
            print('set player.measure_skill to', player.measure_skill)
    # randomize avatar condition
    # Now always set to avatar treatment
    for player in subsession.get_players():
        # player.avatar = random.choice(['yes', 'no'])
        player.avatar = 'yes'
        print('set player.avatar to', player.avatar)


# PAGES
class Introduction(Page):
    pass
    form_model = 'player'
    form_fields = ['accept_instructions']


class Choice(Page):
    form_model = 'player'
    form_fields = [
        'accept_character',
        'intelligence',
        'strength',
        'charisma',
        'agility',
        'stamina',
    ]
    @staticmethod
    def error_message(player: Player, value):
        if value["strength"]+value["intelligence"]+value["charisma"]+value["agility"]+value["stamina"] != 100:
            return 'Please ensure the total allocated points adds up to 100.'

class Results(Page):
    pass


page_sequence = [Introduction, Choice, Results]
