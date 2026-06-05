

from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    
        
            yield f"""<p><b>Scenario: Disease Test Accuracy</b></p>
            
            <p>In a hospital, {C.EXAMPLE_PATIENTS} out of {C.EXAMPLE_TOTAL} patients have Disease X. A diagnostic test correctly identifies the patient's status <b>{C.EXAMPLE_ACCURACY}% of the time</b>.</p>
            
            <p>The test result says:</p>
            <center><i>"Positive for Disease X."</i></center><br>
            
            <p><b>Based on this information: What is the probability that the patient actually has Disease X?</b></p>"""
            yield f"""<p><input type="number" name="practice_estimate" min="0" max="{C.ESTIMATE_MAX}" required> %</p>"""
            for error in components.form['practice_estimate'].errors:
                yield f'<div class="form-control-errors">{error}</div>'
            yield """<p><b>Please briefly explain how you arrived at your answer.</b></p>"""
            yield f"""<p><textarea name="practice_reasoning" required></textarea></p>"""
            for error in components.form['practice_reasoning'].errors:
                yield f'<div class="form-control-errors">{error}</div>'
            yield f"""<p><b>How strongly do you recommend that this patient receive further diagnostic testing?</b></p>
            <p>{C.REC_MIN} (not at all) — {C.REC_MAX} (strongly)</p>"""
            yield components.form_field('practice_recommendation', label='')
            if player.participant.participant_audience == 'public':
                yield "<p>In the main tasks, you will have 1 minute to discuss your recommendation with your group via a chat box.</p>"
            yield """<p><b>If you are ready for the main tasks, please click 'Next'.</b></p>"""
            yield components.next_button()
    


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Practice Task"


# </hook-functions>