

from . import C, current_task, compute_score_and_win, scenario_config, version_for_task


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
        task = current_task(player)
        version = version_for_task(task, player.participant.participant_task_version)
        cfg = scenario_config(task, version)
        acc = C.SCENARIO_ACCURACY
        pool = C.POOL_SIZE
    
        yield f"""<p><b>Scenario: {cfg['title']}</b></p>"""
    
        if task == 'political':
            yield f"""<p>Last year, a violent incident occurred in a residential district of Vienna. The incident was reported to the police, and a suspect was identified based on witness testimony.</p>
        <p>Investigators compiled a suspect pool from individuals with prior records in the district. The pool consisted of {pool:,} people.</p>"""
        else:
            yield f"""<p>A manufacturing facility in Lower Austria produces industrial components. At the end of each production run, components are checked for defects before being approved for shipment.</p>
        <p>A quality control inspector examined a batch of {pool:,} components.</p>"""
    
        yield """<table class="table"><tr><th>Composition</th><th>Count</th><th>Share</th></tr>"""
        for label, count, pct in cfg['rows']:
            yield f"""<tr><td>{label}</td><td>{count}</td><td>{pct}%</td></tr>"""
        yield f"""<tr><td>Total</td><td>{pool}</td><td>{C.PCT_DENOM}%</td></tr></table>"""
    
        if task == 'political':
            yield f"""<p>A witness who was present during the incident was interviewed. This witness correctly identifies the right person <b>{acc}% of the time</b> in situations like this.</p>
        <p>The witness stated:</p>"""
        else:
            yield f"""<p>One component was selected at random and examined by an automated sensor. This sensor correctly identifies whether a component is defective or not <b>{acc}% of the time</b>.</p>
        <p>The sensor reported:</p>"""
    
        yield f"""<center><i>"{cfg['witness']}"</i></center><br>"""
    
        if task == 'political':
            yield f"""<p><b>Based on this information: What is the probability that the perpetrator was actually not an Austrian citizen?</b></p>"""
        else:
            yield f"""<p><b>Based on this information: What is the probability that the component is {cfg['ask']}?</b></p>"""
    
        estimate_field = 'main_estimate' if task == 'political' else 'filler_estimate'
        yield f"""<p><input type="number" name="{estimate_field}" min="0" max="{C.ESTIMATE_MAX}" required> %</p>"""
        for error in components.form[estimate_field].errors:
            yield f'<div class="form-control-errors">{error}</div>'
        yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Main Task"


# </hook-functions>