from . import C, cu


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    yield f"""<p>
            For the main tasks, your payment depends on how accurate your estimate is — the closer you are to the true value, the more money you earn. You can earn up to €{int(2 * C.TASK_BONUS)} in total across both tasks.
        </p>
        
        <details>
            <summary><b>Show detailed scoring rules</b></summary>
            <table class="table table-striped">
                <tr>
                    <th>Deviation from correct answer</th>
                    <th>Score (= % chance of €{int(C.TASK_BONUS)} bonus)</th>
                </tr>
                <tr><td>{C.DEV_0} percentage points</td><td>{C.CHANCE_100}%</td></tr>
                <tr><td>{C.DEV_5} percentage points</td><td>{C.CHANCE_95}%</td></tr>
                <tr><td>{C.DEV_10} percentage points</td><td>{C.CHANCE_80}%</td></tr>
                <tr><td>{C.DEV_15} percentage points</td><td>{C.CHANCE_55}%</td></tr>
                <tr><td>{C.DEV_20} percentage points</td><td>{C.CHANCE_20}%</td></tr>
                <tr><td>{C.DEV_21} percentage points</td><td>{C.CHANCE_12}%</td></tr>
                <tr><td>{C.DEV_22} percentage points</td><td>{C.CHANCE_3}%</td></tr>
                <tr><td>≥{C.DEV_23} percentage points</td><td>{C.CHANCE_0}%</td></tr>
            </table>
        </details>
        
        <br>
        <p>Before the main tasks begin, you will complete a short practice task to get familiar with the format. Your answers there do not count toward your payment.</p>"""
    yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Part 2: Payment Scheme"


# </hook-functions>