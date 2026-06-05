from otree.api import url_of_static, url_of_upload


from . import C, current_task


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    task = current_task(player)
    if task == 'political':
        question = "How strongly do you recommend further investigation of the suspect?"
    else:
        question = "How strongly do you recommend withdrawing this component for further quality inspection?"
    yield f"<p><b>{question}</b></p>"
    yield f"<p>{C.REC_MIN} (not at all) — {C.REC_MAX} (strongly)</p>"
    yield components.form_field('recommendation')
    yield components.chat()
    yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Your Group's Recommendation"


# </hook-functions>