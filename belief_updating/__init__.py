from otree.api import (
    cu,
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    WaitPage,
    Page,
)
import units

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'belief_updating'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # user-defined constants
    MAX_SEAT = 32
    PRIOR_MAX = 100
    Q1_MAX = 50
    Q2_MAX = 100
    Q3_MAX = 70
    Q4_MAX = 100
    Q1_ANSWER = 30
    Q2_ANSWER = 25
    Q3_ANSWER = 20
    Q4_ANSWER = 50
    NUM_SCORE_MAX = 4
    BONUS_PER_CORRECT = 1
    TOWN_POPULATION = 1000
    CHOIR_MEMBERS = 500
    CHOIR_MEN = 100
    NON_CHOIR_MEN = 300
    RED_PCT = 20
    BROWN_PCT = 50
    WHITE_PCT = 30
    RED_POISON_PCT = 20
    NON_RED_POISON_PCT = 5
    FIVE_SIDED = 5
    SIX_SIDED = 6
    ODD_1 = 1
    ODD_3 = 3
    ODD_5 = 5
    DIE_FACE_6 = 6
    Q3_LABEL = 3
    Q4_LABEL = 4
    GROUP_SIZE = 3
    VERSION_THRESHOLD = 45
    VERSION_A_BASE_RATE = 12
    VERSION_B_BASE_RATE = 88
    GROUP_NAME_TIMEOUT = 60
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    seat_number = models.IntegerField(label='Booth number', max=C.MAX_SEAT, min=1)
    prior_estimate = models.IntegerField(label='Your estimate:', max=C.PRIOR_MAX, min=0)
    task_version = models.StringField(choices=['A', 'B'])
    num_q1 = models.IntegerField(label='Your answer', max=C.Q1_MAX, min=0)
    num_q2 = models.IntegerField(label='Your answer', max=C.Q2_MAX, min=0)
    num_q3 = models.IntegerField(label='Your answer', max=C.Q3_MAX, min=0)
    num_q4 = models.IntegerField(label='Your answer', max=C.Q4_MAX, min=0)
    num_score = models.IntegerField()
    numeracy_bonus = models.CurrencyField()
    audience = models.StringField(choices=['public', 'private'])
    public_group_id = models.IntegerField()
    task_order = models.StringField(choices=['political_first', 'neutral_first'])
    group_name = models.StringField(label='Your group name:')
    character_name = models.StringField(label='Your character name:')
# the below function(s) are user-defined, not called by oTree
# <helper-functions>
def assign_audience(players):
    import random
    shuffled = list(players)
    random.shuffle(shuffled)
    half = len(shuffled) // 2
    for p in shuffled[:half]:
        p.audience = 'public'
    for p in shuffled[half:]:
        p.audience = 'private'
def assign_public_groups(players):
    public_players = [p for p in players if p.audience == 'public']
    public_players.sort(key=lambda p: p.prior_estimate)
    
    gid = 1
    for i in range(0, len(public_players), C.GROUP_SIZE):
        chunk = public_players[i:i + C.GROUP_SIZE]
        if len(chunk) == C.GROUP_SIZE:
            for p in chunk:
                p.public_group_id = gid
            gid += 1
        else:
            for p in chunk:
                p.audience = 'private'
def propagate_participant_fields(players):
    import random
    public_group_orders = {}
    for p in players:
        p.participant.participant_number = p.seat_number
        p.participant.participant_audience = p.audience
        if p.audience == 'public':
            gid = p.public_group_id
            if gid not in public_group_orders:
                public_group_orders[gid] = random.choice(['political_first', 'neutral_first'])
            p.task_order = public_group_orders[gid]
            p.participant.public_group_id = gid
        else:
            p.task_order = random.choice(['political_first', 'neutral_first'])
            p.participant.public_group_id = 0
        p.participant.participant_task_order = p.task_order
def setup_estimation_groups(session):
    # Build the Part 2 (estimation_tasks) group structure now, while every
    # participant is synchronised at this wait page and public_group_id has just
    # been assigned. Doing it here means Part 2 needs no all-players wait page:
    # each public group only waits for its own members on the group pages, and
    # one group finishing early never holds up another.
    for ss in session.get_subsessions():
        if ss.get_folder_name() != 'estimation_tasks':
            continue
        groups = {}
        for p in ss.get_players():
            pgid = p.participant.public_group_id
            groups.setdefault(pgid, []).append(p)
        ss.set_group_matrix(list(groups.values()))
# </helper-functions>
class Welcome(Page):
    form_model = 'player'
    form_fields = ['seat_number']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(seat_number=1), button_label='Begin')]
class Part1Intro(Page):
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(), button_label='Next')]
class Background(Page):
    form_model = 'player'
    form_fields = ['prior_estimate']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(prior_estimate=60), button_label='Continue')]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.prior_estimate > C.VERSION_THRESHOLD:
            player.task_version = 'A'
        elif player.prior_estimate < C.VERSION_THRESHOLD:
            player.task_version = 'B'
        else:
            import random
            player.task_version = random.choice(['A', 'B'])
        player.participant.participant_task_version = player.task_version
class Numeracy(Page):
    form_model = 'player'
    form_fields = ['num_q1', 'num_q2', 'num_q3', 'num_q4']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(num_q1=30, num_q2=25, num_q3=20, num_q4=50), button_label='Continue')]
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        score = 0
        if player.num_q1 == C.Q1_ANSWER:
            score += 1
        if player.num_q2 == C.Q2_ANSWER:
            score += 1
        if player.num_q3 == C.Q3_ANSWER:
            score += 1
        if player.num_q4 == C.Q4_ANSWER:
            score += 1
        player.num_score = score
        player.numeracy_bonus = cu(score * C.BONUS_PER_CORRECT)
        player.participant.numeracy_bonus = player.numeracy_bonus
class GroupingWait(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        assign_audience(players)
        assign_public_groups(players)
        propagate_participant_fields(players)
        setup_estimation_groups(group.session)
class EndOfPart1(Page):
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(), button_label='Continue')]
class NameSetup(Page):
    form_model = 'player'
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [
            dict(fields=dict(character_name='Alex'), button_label='Alex (private)'),
            dict(fields=dict(group_name='Team Alpha'), button_label='Team Alpha (public)'),
        ]
    @staticmethod
    def get_form_fields(player: Player):
        if player.audience == 'public':
            return ['group_name']
        else:
            return ['character_name']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.audience == 'public':
            player.participant.group_name = player.group_name
    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.audience == 'public':
            return C.GROUP_NAME_TIMEOUT
page_sequence = [Welcome, Part1Intro, Background, Numeracy, GroupingWait, EndOfPart1, NameSetup]