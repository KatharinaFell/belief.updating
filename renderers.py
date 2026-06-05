from pathlib import Path

_GLOBAL_STYLES_PATH = Path(__file__).parent / '_static' / 'global-styles.css'


def global_styles_block(*args, **kwargs):
    css = _GLOBAL_STYLES_PATH.read_text('utf8')
    yield f'''<style>
{css}
</style>'''
    yield '''<script src="/_static/otai-utils.js"></script>'''
