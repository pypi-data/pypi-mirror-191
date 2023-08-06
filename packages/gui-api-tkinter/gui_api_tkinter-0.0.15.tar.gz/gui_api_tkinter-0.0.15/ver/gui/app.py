import signal

from gui_api_tkinter.lib.guiapi.gui_api_tkinter import GuiApiTinker
from ver.gui import mvc
from ver.gui.cfg import Cfg
from ver.gui.model import Model
from ver.gui.view import View


# --------------------
## holds all objects needed for the GUI app
class App:
    # --------------------
    ## constructor
    def __init__(self):
        mvc.cfg = Cfg()
        mvc.cfg.init()

        if mvc.cfg.logger_type == 'mock':
            from ver.helpers.logger_mock import Logger
        elif mvc.cfg.logger_type == 'stdout':
            from ver.helpers.logger_stdout import Logger
        elif mvc.cfg.logger_type == 'file':
            from ver.helpers.logger_file import Logger

        mvc.logger = Logger()
        mvc.logger.init()

        mvc.view = View()

        mvc.guiapi = GuiApiTinker()
        if mvc.cfg.do_callback:
            cb = mvc.view.callback
        else:
            cb = None
        mvc.guiapi.init(ip_address=mvc.cfg.guiapi_ip_address,
                        ip_port=mvc.cfg.guiapi_ip_port,
                        logger=mvc.logger,
                        verbose=False,
                        callback=cb)

        ## holds reference to the GUI/tkinter object
        mvc.model = Model()
        mvc.model.init()

        ## holds reference to the GUI/tkinter object
        mvc.view.init()

    # --------------------
    ## initialization of objects
    #
    # @return None
    def init(self):
        mvc.model.clear()

        # Set CTRL-C handler
        signal.signal(signal.SIGINT, mvc.view.abort)

        # start tk event handler (does not return)
        mvc.view.start_mainloop()
        # does not return
