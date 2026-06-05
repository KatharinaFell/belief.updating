from otree.api import (
    Currency,
    cu,
    currency_range,
    models,
    fields,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    ExtraModel,
    WaitPage,
    Page,
    read_csv,
)
import units

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'estimation_tasks'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    # user-defined constants
    P_STAR_VERSION_A = 29
    P_STAR_VERSION_B = 71
    ESTIMATE_MAX = 100
    MC_MAX = 4
    POOL_SIZE = 1000
    SCENARIO_ACCURACY = 75
    BASE_RATE_LOW = 12
    BASE_RATE_HIGH = 88
    PCT_DENOM = 100
    TASK_BONUS = cu(6)
    SCORE_COEFFICIENT = 0.2
    EX_DEV_0 = 0
    EX_DEV_5 = 5
    EX_DEV_10 = 10
    EX_DEV_15 = 15
    EX_DEV_20 = 20
    EX_DEV_21 = 21
    EX_DEV_22 = 22
    EX_DEV_23 = 23
    NUM_SCORE_MAX = 4
    BONUS_PER_CORRECT = 1
    FIXED_PAYMENT = cu(21)
    BONUS_CHANCE_EXAMPLE = 80
    DEV_0 = 0
    DEV_5 = 5
    DEV_10 = 10
    DEV_15 = 15
    DEV_20 = 20
    DEV_23 = 23
    CHANCE_100 = 100
    CHANCE_95 = 95
    CHANCE_80 = 80
    CHANCE_55 = 55
    CHANCE_20 = 20
    CHANCE_0 = 0
    DEV_21 = 21
    DEV_22 = 22
    CHANCE_12 = 12
    CHANCE_3 = 3
    EXAMPLE_PATIENTS = 200
    EXAMPLE_TOTAL = 1000
    EXAMPLE_ACCURACY = 80
    REC_MIN = 1
    REC_MAX = 7
    PUBLIC_REC_TIMEOUT = 60
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    group_recommendation = models.IntegerField(max=C.REC_MAX, min=C.REC_MIN)
class Player(BasePlayer):
    main_estimate = models.IntegerField(max=C.ESTIMATE_MAX, min=0)
    filler_estimate = models.IntegerField(max=C.ESTIMATE_MAX, min=0)
    main_justification = models.LongStringField(label='')
    filler_justification = models.LongStringField(label='')
    p_star = models.IntegerField()
    main_score = models.FloatField()
    filler_score = models.FloatField()
    main_won = models.BooleanField()
    filler_won = models.BooleanField()
    total_bonus = models.CurrencyField()
    mc_score = models.IntegerField(choices=[[0, 'Not at all'], [1, 'Slightly'], [2, 'Moderately'], [3, 'Much'], [4, 'Very much']], label='To what extent is your attitude about immigration a reflection of your core moral beliefs and convictions?', max=C.MC_MAX, min=0, widget=widgets.RadioSelect)
    practice_estimate = models.IntegerField(label='Your estimate:', max=C.ESTIMATE_MAX, min=0)
    practice_reasoning = models.LongStringField(label='Please briefly explain how you arrived at your answer.')
    recommendation = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7], max=C.REC_MAX, min=C.REC_MIN, widget=widgets.RadioSelectHorizontal)
    practice_recommendation = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7], label='How strongly do you recommend that this patient receive further diagnostic testing?', max=C.REC_MAX, min=C.REC_MIN, widget=widgets.RadioSelectHorizontal)
# built-in hook function(s) (called automatically by oTree)
# <hook-functions>
def main_justification_error_message(player: Player, value):
    if value.isdigit():
        return "Please provide a text explanation, not just a number."
def filler_justification_error_message(player: Player, value):
    if value.isdigit():
        return "Please provide a text explanation, not just a number."
# </hook-functions>
# the below function(s) are user-defined, not called by oTree
# <helper-functions>
def current_task(player: Player):
    task_order = player.participant.participant_task_order
    if task_order == 'political_first':
        return 'political' if player.round_number == 1 else 'neutral'
    else:
        return 'neutral' if player.round_number == 1 else 'political'
def get_group_peers(player: Player):
    participants = player.session.get_participants()
    peers = []
    for p in participants:
        if p.public_group_id == player.participant.public_group_id and p.code != player.participant.code:
            peers.append(p)
    return peers
def compute_score(estimate, p_star):
    return max(C.PCT_DENOM - C.SCORE_COEFFICIENT * (estimate - p_star) ** 2, 0)
def compute_score_and_win(estimate, p_star):
    import random
    score = compute_score(estimate, p_star)
    r = random.uniform(0, C.PCT_DENOM)
    return score, score >= r
def bonus_for_task(won):
    return C.TASK_BONUS if won else cu(0)
def scenario_config(task, version):
    pool = C.POOL_SIZE
    low_count = pool * C.BASE_RATE_LOW // C.PCT_DENOM
    high_count = pool * C.BASE_RATE_HIGH // C.PCT_DENOM
    configs = {
        ('political', 'A'): dict(
            title="A Criminal Incident in Vienna",
            rows=[
                ("Suspects who are not Austrian citizens", low_count, C.BASE_RATE_LOW),
                ("Suspects who are Austrian citizens", high_count, C.BASE_RATE_HIGH),
            ],
            witness="The perpetrator was not an Austrian citizen.",
            ask="not an Austrian citizen",
        ),
        ('political', 'B'): dict(
            title="A Criminal Incident in Vienna",
            rows=[
                ("Suspects who are not Austrian citizens", high_count, C.BASE_RATE_HIGH),
                ("Suspects who are Austrian citizens", low_count, C.BASE_RATE_LOW),
            ],
            witness="The perpetrator was an Austrian citizen.",
            ask="not an Austrian citizen",
        ),
        ('neutral', 'A'): dict(
            title="Quality Control at a Production Facility",
            rows=[
                ("Components with a defect", low_count, C.BASE_RATE_LOW),
                ("Components without a defect", high_count, C.BASE_RATE_HIGH),
            ],
            witness="This component is defective.",
            ask="actually defective",
        ),
        ('neutral', 'B'): dict(
            title="Quality Control at a Production Facility",
            rows=[
                ("Components with a defect", high_count, C.BASE_RATE_HIGH),
                ("Components without a defect", low_count, C.BASE_RATE_LOW),
            ],
            witness="This component is NOT defective.",
            ask="actually defective",
        ),
    }
    return configs[(task, version)]
def current_round_estimate(player: Player):
    task = current_task(player)
    if task == 'political':
        return player.main_estimate
    return player.filler_estimate
def get_group_players(player: Player):
    my_pgid = player.participant.public_group_id
    result = []
    for p in player.subsession.get_players():
        if p.participant.public_group_id == my_pgid:
            result.append(p)
    return result
def version_for_task(task, participant_version):
    return participant_version
# </helper-functions>
class PaymentScheme(Page):
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(), button_label='Continue')]
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class ExampleTask(Page):
    form_model = 'player'
    form_fields = ['practice_estimate', 'practice_reasoning', 'practice_recommendation']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        
        return [dict(fields=dict(practice_estimate=50, practice_reasoning='test', practice_recommendation=5), button_label='Submit')]
        
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
class EstimationTask(Page):
    form_model = 'player'
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        
        return [dict(fields=dict(main_estimate=50, filler_estimate=50), button_label='Submit')]
        
    @staticmethod
    def get_form_fields(player: Player):
        
        task = current_task(player)
        if task == 'political':
            return ['main_estimate']
        else:
            return ['filler_estimate']
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        task = current_task(player)
        version = version_for_task(task, player.participant.participant_task_version)
        player.p_star = C.P_STAR_VERSION_A if version == 'A' else C.P_STAR_VERSION_B
        
        if task == 'political':
            score, won = compute_score_and_win(player.main_estimate, player.p_star)
            player.main_score = score
            player.main_won = won
        else:
            score, won = compute_score_and_win(player.filler_estimate, player.p_star)
            player.filler_score = score
            player.filler_won = won
        
        if player.round_number == 2:
            prev = player.in_round(1)
            if current_task(prev) == 'political':
                participant_main_estimate = prev.main_estimate
                participant_filler_estimate = player.filler_estimate
                bonus1 = bonus_for_task(prev.main_won)
            else:
                participant_main_estimate = player.main_estimate
                participant_filler_estimate = prev.filler_estimate
                bonus1 = bonus_for_task(prev.filler_won)
            player.participant.main_estimate = participant_main_estimate
            player.participant.filler_estimate = participant_filler_estimate
            player.participant.bonus_task1 = bonus1
        
            task2 = current_task(player)
            task2_won = player.main_won if task2 == 'political' else player.filler_won
            bonus2 = bonus_for_task(task2_won)
            player.participant.bonus_task2 = bonus2
        
            player.total_bonus = C.FIXED_PAYMENT + player.participant.numeracy_bonus + bonus1 + bonus2
            player.participant.payoff = player.total_bonus
class EstimationJustification(Page):
    form_model = 'player'
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(main_justification='test just', filler_justification='test just'), button_label='Submit')]
    @staticmethod
    def get_form_fields(player: Player):
        task = current_task(player)
        if task == 'political':
            return ['main_justification']
        else:
            return ['filler_justification']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        task = current_task(player)
        if task == 'political':
            player.participant.main_justification = player.main_justification
        else:
            player.participant.filler_justification = player.filler_justification
class PrivateRecommendation(Page):
    form_model = 'player'
    form_fields = ['recommendation']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(recommendation=5), button_label='Recommend 5')]
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.participant_audience == 'private'
class PeerEstimatesWait(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.participant_audience == 'public'
class PeerEstimates(Page):
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(), button_label='Next')]
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.participant_audience == 'public'
class PublicRecommendation(Page):
    form_model = 'player'
    form_fields = ['recommendation']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(recommendation=5), button_label='Recommend 5')]
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.participant_audience == 'public'
    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.PUBLIC_REC_TIMEOUT
    @staticmethod
    def process_form_on_timeout(player: Player, form):
        if form.recommendation.data is not None:
            player.recommendation = form.recommendation.data
class PublicRecommendationWait(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.participant_audience == 'public'
    @staticmethod
    def after_all_players_arrive(group: Group):
        from collections import Counter
        players = group.get_players()
        valid = [p for p in players if p.recommendation is not None]
        if not valid:
            return
        counts = Counter(p.recommendation for p in valid)
        max_count = max(counts.values())
        if max_count > len(valid) // 2:
            winner = next(v for v, c in counts.items() if c == max_count)
        else:
            # No majority - use the highest id_in_group as tiebreaker
            last = max(valid, key=lambda p: p.id_in_group)
            winner = last.recommendation
        group.group_recommendation = winner
class MoralConviction(Page):
    form_model = 'player'
    form_fields = ['mc_score']
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(mc_score=3), button_label='Much')]
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2
class FinalPayment(Page):
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(), button_label='Next')]
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2
class End(Page):
    @staticmethod
    def bot_available_submissions(id_in_group, round_number, session_config):
        return [dict(fields=dict(), button_label='Next')]
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time
        player.participant.stopped_at = time.time()
page_sequence = [PaymentScheme, ExampleTask, EstimationTask, EstimationJustification, PrivateRecommendation, PeerEstimatesWait, PeerEstimates, PublicRecommendation, PublicRecommendationWait, MoralConviction, FinalPayment, End]