from otree.api import models
import units
PARTICIPANT_FIELDS = dict(
    bonus_task1 = models.CurrencyField(),
    bonus_task2 = models.CurrencyField(),
    filler_estimate = models.IntegerField(),
    filler_justification = models.LongStringField(label=''),
    group_name = models.StringField(label='Group name'),
    main_estimate = models.IntegerField(),
    main_justification = models.LongStringField(label=''),
    numeracy_bonus = models.CurrencyField(),
    participant_audience = models.StringField(choices=['public', 'private']),
    participant_number = models.IntegerField(),
    participant_task_order = models.StringField(choices=['political_first', 'neutral_first']),
    participant_task_version = models.StringField(choices=['A', 'B']),
    public_group_id = models.IntegerField(),
)
SESSION_FIELDS = dict(
)