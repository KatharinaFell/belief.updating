from otree.api import url_of_static, url_of_upload


from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    if player.audience == 'public':
        yield """<p>You have 2 minutes to agree on a group name with your group. Type freely in the chat below. Once you have agreed, enter your group name in the field below and click confirm.</p>"""
        yield components.chat(channel=f"group_name_{player.public_group_id}")
        yield components.form_field('group_name')
    else:
        yield """<p>Please decide on a character name for this session.</p>"""
        yield components.form_field('character_name')
    yield """<button type="submit" class="otree-btn-next">Confirm</button>"""


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    if player.audience == 'public':
        yield "Group Task"
    else:
        yield "Character Name"


# </hook-functions>