import math
import json
import random
from tmux_projector.utils import run_command
from tmux_projector.models.pane import Pane
from tmux_projector.exceptions import SliceException
from tmux_projector.models.options import OptionsManager

class Window:

    def __init__(self, window_name, session_name, options=None):
        self.window_name = window_name
        self.session_name = session_name
        self.panes = []
        self.options = {}
        self.options_manager = OptionsManager(session_name, options)

    @staticmethod
    def from_json(window_json, session_name):
        window = Window(window_json['window_name'], session_name)
        if 'layout' in window_json:
            window.set_option('layout', window_json['layout'])
        return window
        
    def get_option(self, option):
        return self.options_manager.get_option(option)

    def create_pane(self):
        pane = Pane(len(self.panes)+1, self.window_name, self.session_name)
        self.panes.append(pane)
        return pane

    def start(self, window_index):
        self._start_window(window_index)
        for pane_index, pane in enumerate(self.panes):
            pane.start()
        self._cleanup()
        self._set_layout()

    def set_option(self, option, value):
        self.options[option] = value

    def to_json(self):
        panes = [pane.to_json() for pane in self.panes]
        data = {'window_name': self.window_name, 'layout': self.get_option('layout'), 'panes': panes}
        return data 

    def _set_layout(self):
        if 'layout' in self.options:
            layout_command = f'tmux select-layout -t {self.session_name}:{self.window_name} {self.options["layout"]}'
            run_command(layout_command)

    def _start_window(self, window_index):
        create_window_command = f"tmux new-window -t {self.session_name}:{window_index} -n {self.window_name}"
        run_command(create_window_command)


    def _cleanup(self):
        ## Removing the first unnecessary pane created when creating this window
        kill_pane_command = f"tmux kill-pane -t {self.session_name}:{self.window_name}.0"
        run_command(kill_pane_command)




