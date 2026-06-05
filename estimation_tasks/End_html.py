from otree.api import url_of_static, url_of_upload


from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield """<p>Thank you for your participation.</p>
    <p>Please remain seated and wait quietly until your participant number is called out for payment.</p>"""


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield ""


# </hook-functions>