from tmux_projector.utils import run_command

class OptionsManager:

    def __init__(self, session_name, options):
        self.session_name = session_name
        self.options = options if options else {}

    def apply_options(self):
        self._apply_mouse()

    def set_option(self, option, value):
        self.options[option] = value

    def get_option(self, option):
        return self.options.get(option, None)

    def _apply_mouse(self):
        mouse_enabled = self.get_option('mouse')
        if mouse_enabled != None:
            value = 'on' if mouse_enabled else 'off'
            mouse_command = f'tmux set -g mouse {value}'
            run_command(mouse_command)

    def to_json(self):
        return self.options
