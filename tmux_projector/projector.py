import yaml
import io
import os
import json
from tmux_projector.utils import run_command
from tmux_projector.models.session import Session
from tmux_projector.validator import ConfigValidator
from tmux_projector.exceptions import MissingGlobalConfigException


class TmuxProjector:

    def __init__(self):
        pass


    def initialize_project(self):
        """
        Creates a barebones project and saves it as a YAML file.
        """ 
        session = Session(session_name='test')
        session.add_option('auto_attach', True)
        window = session.create_window({'window_name': 'test-window', 'layout': None})
        pane = window.create_pane()
        pane.dir = os.getcwd()
        pane.cmd = 'echo test'


        self._save_config(session.to_json())

    def run(self, args):
        config_path = '.tmux_projector.yaml'
        if os.path.exists(config_path):
            self._start_project(config_path, args)
            
        else:
            print("No project config found. Initialize one by running 'tmux_projector init'")

    def run_global_project(self, args):
        """
        Attempts to start a 'global' ts project. That is, a project that has been saved to global entries so that it can be ran from anywhere.
        """
        global_file = self._get_global_project_config()
        if os.path.exists(global_file):
            for line in open(global_file).readlines():
                project_name, project_path = line.strip().split("\t")
                if project_name == args.name:
                    self._start_project(project_path, args)
                    return
            raise MissingGlobalConfigException(f'Did not found a global config with name: {args.name}')
        else:
            raise MissingGlobalConfigException(f'Did not found a global config with name: {args.name}')



    def kill(self):
        if os.path.exists('.tmux_projector.yaml'):
            session = self._load_config()
            running_sessions = self._get_running_sessions()
            if session.session_name in running_sessions:
                session.kill()


    def set_project_as_global(self, args):
        global_file = self._get_global_project_config()
        if os.path.exists(global_file):
            current_projects = open(global_file).readlines()
        else:
            current_projects = []
        current_projects.append(f'{args.name}\t{os.getcwd()}/.tmux_projector.yaml\n')
        open(global_file, "w").writelines(current_projects)


    def _load_config(self, path):
        session_json = yaml.load(open(path), Loader=yaml.FullLoader)
        validator = ConfigValidator().validate(session_json)
        session = Session.from_json(session_json)
        return session 

    def _start_project(self, config_path, args):
        session = self._load_config(config_path)
        running_sessions = self._get_running_sessions()
        if session.session_name in running_sessions:
            if args.restart:
                session.kill()
                session.start()
            else:
                self._reconnect_to_session(session)
        else:
            session.start()

    def _save_config(self, data):
        open('.tmux_projector.yaml', 'w').write(yaml.dump(data, sort_keys=False))


    def _get_running_sessions(self):
        tmux_ls_command = f'tmux ls'
        output = run_command(tmux_ls_command)
        sessions = set()
        for line in output.split("\n"):
            if not line.strip(): continue
            session_name = line.split(":")[0]
            sessions.add(session_name)
        return sessions

    def _get_global_project_config(self):
        global_file = os.path.join(os.path.expanduser('~'), '.tmux_projector_globals.yaml')
        return global_file


    def _reconnect_to_session(self, session):
        if session.get_option('auto_attach'):
            self._reattach(session)
        else:
            print(f"Session {session.session_name} is already running. Do you want to reattach to it?")
            decision = input('y/n: ')
            if decision.lower() == 'y':
                self._reattach(session)

    def _reattach(self, session):
        reattach_command = f'tmux attach -t {session.session_name}'
        run_command(reattach_command)

    
