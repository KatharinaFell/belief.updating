from otree.api import url_of_static, url_of_upload


from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    
        if player.audience == 'public':
            yield """<p>Thank you for completing Part 1.</p>
        <p>You have been grouped with the two participants whose estimates of the share of convicted criminals without Austrian citizenship were most similar to yours.</p>
        <p>Before starting Part 2, you and your group will have 1 minute to agree on a group name together.</p>
        <p>When you are ready, click Continue.</p>"""
        else:
            yield """<p>Thank you for completing Part 1.</p>
        <p>Before starting Part 2, you will choose a character name for this session.</p>
        <p>When you are ready, click Continue.</p>"""
        yield """<button type="submit" class="otree-btn-next">Continue</button>"""
    


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "End of Part 1"


# </hook-functions>