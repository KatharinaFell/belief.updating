

from . import C


# built-in hook renderer(s) (called automatically by oTree)


# <hook-functions>


def content_block(player, components, **api_kwargs):
    fixed = int(C.FIXED_PAYMENT)
    numeracy = int(player.participant.numeracy_bonus)
    task1 = int(player.participant.bonus_task1)
    task2 = int(player.participant.bonus_task2)
    total = int(player.total_bonus)
    yield f"""
        <table class="table table-bordered" style="max-width:480px;">
            <thead>
                <tr><th>Component</th><th>Amount</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>Fixed payment</td>
                    <td>€{fixed}</td>
                </tr>
                <tr>
                    <td>Mathematical questions (out of €{C.NUM_SCORE_MAX})</td>
                    <td>€{numeracy}</td>
                </tr>
                <tr>
                    <td>Task 1</td>
                    <td>€{task1}</td>
                </tr>
                <tr>
                    <td>Task 2</td>
                    <td>€{task2}</td>
                </tr>
                <tr class="table-active">
                    <td><strong>Total</strong></td>
                    <td><strong>€{total}</strong></td>
                </tr>
            </tbody>
        </table>"""
    yield components.next_button()


def meta_title_block(player, components, **api_kwargs):
    yield ""


def title_block(player, components, **api_kwargs):
    yield "Final Payment"


# </hook-functions>
