

from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield """<p>Please make sure you have read the printed instructions before continuing.</p>
    <p>When you are ready to start the experiment, please enter your booth number below and click Begin.</p>"""
    yield components.form_field('seat_number')
    yield """<button type="submit" class="otree-btn-next">Begin</button>"""


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Welcome"


# </hook-functions>