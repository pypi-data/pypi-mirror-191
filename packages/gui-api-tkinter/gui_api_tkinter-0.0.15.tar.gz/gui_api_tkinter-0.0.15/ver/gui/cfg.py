from ver.gui.cli import Cli


# --------------------
## holds configuration information
class Cfg:
    # --------------------
    ## constructor
    def __init__(self):
        ## the IP address to use for socket comms
        self.guiapi_ip_address = '127.0.0.1'
        ## the IP port to use for socket comms
        self.guiapi_ip_port = 5001
        ## whether logging is verbose or not
        self.verbose = True
        ## flag indicates whether to do callback function or not
        self.do_callback = True
        ## type of logger to use
        self.logger_type = 'mock'

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        cli = Cli()
        cli.init()
