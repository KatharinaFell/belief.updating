from otree.api import url_of_static, url_of_upload


from . import C, current_task


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    
        task = current_task(player)
        field_name = 'main_justification' if task == 'political' else 'filler_justification'
        
        yield """<p><b>Please briefly explain how you arrived at your answer.</b></p>
    <p>For example: did you use the numbers provided, rely on your general impression, or something else?</p>"""
        yield components.form_field(field_name)
        yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield ""


# </hook-functions>