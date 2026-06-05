

from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield f"""<p>Please answer the following four questions. You earn &euro;{C.BONUS_PER_CORRECT} for each correct answer, up to &euro;{C.NUM_SCORE_MAX * C.BONUS_PER_CORRECT} in total. You may use the pen and paper provided.</p>
    
    <p><i>Question 1.</i> Imagine a five-sided die is thrown {C.Q1_MAX} times. On average, out of these {C.Q1_MAX} throws, how many times would this five-sided die show an odd number ({C.ODD_1}, {C.ODD_3} or {C.ODD_5})?</p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" name="num_q1" min="0" max="{C.Q1_MAX}" required> out of {C.Q1_MAX} throws</p>
    """
    for error in components.form['num_q1'].errors:
        yield f'<div class="form-control-errors">{error}</div>'
    yield f"""<p><i>Question 2.</i> Out of {C.TOWN_POPULATION:,} people in a small town, {C.CHOIR_MEMBERS:,} are members of a choir. Out of these {C.CHOIR_MEMBERS:,} members in the choir {C.CHOIR_MEN} are men. Out of the {C.CHOIR_MEMBERS:,} inhabitants that are not in the choir {C.NON_CHOIR_MEN} are men. What is the probability that a randomly drawn man is a member of the choir?</p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" name="num_q2" min="0" max="{C.Q2_MAX}" required> %</p>
    """
    for error in components.form['num_q2'].errors:
        yield f'<div class="form-control-errors">{error}</div>'
    yield f"""<p><i>Question {C.Q3_LABEL}.</i> Imagine a six-sided die is thrown. The probability that the die shows a {C.DIE_FACE_6} is twice as high as the probability of each of the other numbers. On average, out of these {C.Q3_MAX} throws, how many times would the die show the number {C.DIE_FACE_6}?</p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" name="num_q3" min="0" max="{C.Q3_MAX}" required> out of {C.Q3_MAX} throws</p>
    """
    for error in components.form['num_q3'].errors:
        yield f'<div class="form-control-errors">{error}</div>'
    yield f"""<p><i>Question {C.Q4_LABEL}.</i> In a forest, {C.RED_PCT}% of mushrooms are red, {C.BROWN_PCT}% brown, and {C.WHITE_PCT}% white. A red mushroom is poisonous with a probability of {C.RED_POISON_PCT}%. A mushroom that is not red is poisonous with a probability of {C.NON_RED_POISON_PCT}%. What is the probability that a poisonous mushroom in the forest is red?</p>
    <p>&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" name="num_q4" min="0" max="{C.Q4_MAX}" required> %</p>
    """
    for error in components.form['num_q4'].errors:
        yield f'<div class="form-control-errors">{error}</div>'
    yield """<button type="submit" class="otree-btn-next">Submit</button>"""


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Mathematical Questions"


# </hook-functions>