

from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield """<p>Part 1 consists of two blocks: a guessing question, followed by four short maths questions.</p>
    <p>When you are ready, click Continue.</p>"""
    yield """<button type="submit" class="otree-btn-next">Continue</button>"""


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Part 1"


# </hook-functions>