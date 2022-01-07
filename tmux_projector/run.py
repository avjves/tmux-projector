import argparse

from tmux_projector.projector import TmuxProjector


def main():
    parser = argparse.ArgumentParser(description='Tmux projector')
    subparser = parser.add_subparsers(help='Action to take', dest='action', required=True)

    init_parser = subparser.add_parser('init')

    start_parser = subparser.add_parser('start')
    start_parser.add_argument('name', help="Name of a specific global project.", nargs='?')
    start_parser.add_argument('--restart', action='store_true')

    kill_parser = subparser.add_parser('kill')

    global_parser = subparser.add_parser('global')
    global_parser.add_argument('--name', help="Name the current project for global usage", required=True)

    args = parser.parse_args()

    projector = TmuxProjector()
    if args.action == 'init':
        projector.initialize_project()
    elif args.action == 'kill':
        projector.kill()
    elif args.action == 'start':
        if args.name:
            projector.run_global_project(args)
        else:
            projector.run(args)
    elif args.action == 'global':
        projector.set_project_as_global(args)
    else:
        pass


if __name__ == "__main__":
    main()
