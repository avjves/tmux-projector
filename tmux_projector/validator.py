import sys
import math
import random
from tmux_projector.exceptions import ValidationException

ALLOWED_LAYOUTS = ['even-horizontal', 'even-vertical', 'main-horizontal', 'main-vertical', 'tiled']

class ConfigValidator:

    def __init__(self):
        pass

    def validate(self, session_json):
        try:
            self._validate_session(session_json)
            self._validate_windows(session_json)
            self._validate_panes(session_json)
            pass
        except ValidationException as e:
            print(e.message)
            sys.exit(1)

    def _validate_session(self, session_json):
        if not session_json.get('session_name', ''):
            raise ValidationException(f'Session requires a name')
        if session_json.get('layout', None):
            if session_json['layout'] not in ALLOWED_LAYOUTS:
                raise ValidationException(f'Layout {session_json["layout"]} not valid.')

    def _validate_windows(self, session_json):
        for window in session_json['windows']:
            pass

    def _validate_panes(self, session_json):
        for window in session_json['windows']:
            for pane in window['panes']:
                pass
