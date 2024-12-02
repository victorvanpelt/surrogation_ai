from os import environ


SESSION_CONFIGS = [
     dict(
         name='chatGPT',
         app_sequence=['chatGPT'],
         num_demo_participants=2,
         prompt=""
     ),
    dict(
        name='Surrogation',
        app_sequence=['surrogation'],
        num_demo_participants=2,
        surrogation="",
    ),
    dict(
        name='dvstudy_experiment_one',
        app_sequence=['dvstudy'],
        num_demo_participants=16,
        surrogation="",
        prompt="",
        ai_condition="",
        prompting=0,
        exploratory=0
    ),
    dict(
        name='dvstudy_experiment_two',
        app_sequence=['dvstudy'],
        num_demo_participants=16,
        surrogation="",
        prompt="",
        ai_condition="",
        prompting=1,
        exploratory=0
    ),
    dict(
        name='dvstudy_experiment_three',
        app_sequence=['dvstudy'],
        num_demo_participants=16,
        surrogation="",
        prompt="",
        ai_condition="",
        prompting=1,
        exploratory=1
    )
]
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.8, doc=""
)

PARTICIPANT_FIELDS = ["condition", "ai_condition", "surrogation", "finished"]
SESSION_FIELDS = ["prolific_completion_url"]


# rooms
ROOMS = [
    dict(
        name='studyRoom1',
        display_name='Study Room 1',
    ),
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6929828123368'
