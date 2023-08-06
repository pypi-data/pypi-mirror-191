import argparse

from ver.gui import mvc


# --------------------
## holds all command line variables
class Cli:

    # --------------------
    ## constructor
    def __init__(self):
        pass

    # --------------------
    def init(self):
        parser = argparse.ArgumentParser(description='ver')

        msg = 'no callback function'
        parser.add_argument('--no-callback', dest='do_callback',
                            default=True, action='store_false',
                            help=msg)

        msg = 'logger type'
        parser.add_argument('--logger', type=str, dest='logger_type',
                            default='mock', help=msg)

        args = parser.parse_args()
        mvc.cfg.do_callback = args.do_callback
        mvc.cfg.logger_type = args.logger_type
