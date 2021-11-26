from collections import OrderedDict

from tmux_projector.utils import run_command
from tmux_projector.utils import debug_print
from tmux_projector.models.window import Window


class Session:

    def __init__(self, session_name, options=None):
        self.session_name = session_name
        self.windows = []
        self.options = options if options else {}

    def add_option(self, option, value):
        self.options[option] = value

    def create_window(self, window_json):
        window = Window.from_json(window_json, self.session_name)
        self.windows.append(window)
        return window

    @staticmethod
    def from_json(session_json):
        session = Session(session_json['session_name'], session_json['options'])
        for window_json in session_json['windows']:
            window = session.create_window(window_json)
            for pane_json in window_json['panes']:
                pane = window.create_pane()
                pane._load_config_from_json(pane_json)
        return session

    def get_option(self, option):
        return self.options.get(option, None)

    def to_json(self):
        windows = [window.to_json() for window in self.windows]
        data = {}
        data['session_name'] = self.session_name
        data['windows'] = windows
        data['options'] = self.options
        return data

    def start(self):
        session_created = self._start_session()
        if session_created:
            for window_i, window in enumerate(self.windows):
                window.start(window_i + 1) # new-session already created a single window
            self._cleanup()

        if self.options.get('auto_attach', False):
            self._attach()
        else:
            print("Session is now ready. Attach to the session by running the command:")
            print(f"tmux attach -t {self.session_name}")

    def kill(self):
        kill_command = f'tmux kill-session -t {self.session_name}'
        run_command(kill_command)


    def _attach(self):
        attach_command = f'tmux attach -t {self.session_name}'
        run_command(attach_command)

    def _cleanup(self):
        ## Removing the first unnecessary window created when creating the session
        kill_window_command = f"tmux kill-window -t {self.session_name}:0"
        run_command(kill_window_command)
        renumber_windows_command = f"tmux move-window -t {self.session_name} -r"
        run_command(renumber_windows_command)

    def _start_session(self):
        start_command = f"tmux new -d -s {self.session_name}"
        run_command(start_command)
        return True



