from otree.api import url_of_static, url_of_upload


from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield components.form_field('mc_score')
    yield """<button type="submit" class="otree-btn-next">Submit</button>"""


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield ""


# </hook-functions>