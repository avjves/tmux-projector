from tmux_projector.utils import run_command
from tmux_projector.models.pane import Pane
class Window:

    def __init__(self, window_name, session_name):
        self.window_name = window_name
        self.session_name = session_name
        self.panes = []

    def create_pane(self):
        pane = Pane(len(self.panes)+1, self.window_name, self.session_name)
        self.panes.append(pane)
        return pane

    def start(self, window_index):
        self._start_window(window_index)
        for pane in self.panes:
            pane.start()
        self._cleanup()

    def to_json(self):
        panes = [pane.to_json() for pane in self.panes]
        data = {'window_name': self.window_name, 'panes': panes}
        return data 

    def _start_window(self, window_index):
        create_window_command = f"tmux new-window -t {self.session_name}:{window_index} -n {self.window_name}"
        run_command(create_window_command)


    def _cleanup(self):
        ## Removing the first unnecessary pane created when creating this window
        kill_pane_command = f"tmux kill-pane -t {self.session_name}:{self.window_name}.0"
        run_command(kill_pane_command)




