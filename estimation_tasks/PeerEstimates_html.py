

from . import C, get_group_players, current_round_estimate, current_task


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    group_players = get_group_players(player)
    task = current_task(player)
    task_label = 'Vienna incident' if task == 'political' else 'Production-facility'
    group_name = player.participant.group_name
    
    yield f"""<p><b>Group: {group_name}</b> — Here are the estimates from your group for the {task_label} scenario.</p>
    <table class="table">
    <tr><th>Participant</th><th>Estimate</th></tr>"""
    for p in group_players:
        est = current_round_estimate(p)
        label = 'You' if p.participant.code == player.participant.code else f'Participant #{p.participant.participant_number}'
        yield f"<tr><td>{label}</td><td>{est}%</td></tr>"
    yield "</table>"
    
    if task == 'political':
        action_text = "recommend further investigation of the suspect"
    else:
        action_text = "recommend withdrawing this component for further quality inspection"
    yield f"<p>On the next page, you will need to decide with your group how strongly you {action_text}. You will have {C.PUBLIC_REC_TIMEOUT} seconds for this task.</p>"
    yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Group Estimates"


# </hook-functions>