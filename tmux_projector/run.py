import argparse

from tmux_projector.projector import TmuxProjector


def main():
    parser = argparse.ArgumentParser(description='Tmux projector')
    subparser = parser.add_subparsers(help='Action to take', dest='action', required=True)

    init_parser = subparser.add_parser('init')

    start_parser = subparser.add_parser('start')
    start_parser.add_argument('--restart', action='store_true')

    kill_parser = subparser.add_parser('kill')

    args = parser.parse_args()

    projector = TmuxProjector()
    if args.action == 'init':
        projector.initialize_project()
    elif args.action == 'kill':
        projector.kill()
    else:
        projector.run(args)


if __name__ == "__main__":
    main()
