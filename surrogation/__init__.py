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
        'main_name',
        'gen_check',
        'seed',
        'save_image',
        'accessory',
        'facial_hair',
        'eye_sight',
        'headgear',
    ]

class Results(Page):
    pass


page_sequence = [Introduction1, Introduction2, Choice, Results]
