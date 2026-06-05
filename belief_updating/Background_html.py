from otree.api import url_of_static, url_of_upload


from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield f"""<p>Statistik Austria publishes annual court statistics on criminal convictions in Austria. Out of every {C.PRIOR_MAX} people convicted of a crime, how many do you think are not Austrian citizens?</p>"""
    yield components.form_field('prior_estimate')
    yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Guessing Question"


# </hook-functions>