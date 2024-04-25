import itertools

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
    intelligence = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    charisma = models.IntegerField(blank=True)
    agility = models.IntegerField(blank=True)
    stamina = models.IntegerField(blank=True)


# FUNCTIONS
def creating_session(subsession: Subsession):
    # randomize to treatments
    # Now always set to surrotation treatment
    treats = itertools.cycle(['yes', 'no'])
    skill_focus = itertools.cycle(['Intelligence', 'Strength', 'Charisma', 'Agility', 'Stamina'])
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


# PAGES
class Introduction(Page):
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
    # @staticmethod
    # def error_message(player: Player, value):
    #     if value["strength"]+value["intelligence"]+value["charisma"]+value["agility"]+value["stamina"] != 100:
    #         return 'Please ensure the total allocated points adds up to 100.'

class Results(Page):
    pass


page_sequence = [Introduction, Choice, Results]
