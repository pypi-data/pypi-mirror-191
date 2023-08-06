from .gui_api_server import GuiApiServer
from .. import services
from ..cfg import Cfg


# --------------------
## holds functions to interact with tkinter and the server
class GuiApiTinker:
    # --------------------
    ## constructor
    def __init__(self):
        ## the top level root window for the GUI
        self._window = None
        ## the top level menu
        self._menu = None
        ## the current screen content
        self._screen = None

        services.guiapi = self
        services.server = GuiApiServer()

    # --------------------
    ## initialize. Configure and start the server
    #
    # @param ip_address   (optional) the socket address for the server
    # @param ip_port      (optional) the socket port for the server
    # @param logger       (optional) reference to a logger object
    # @param verbose      (optional) flag indicating if verbose logging is required
    # @param callback     (optional) reference to callback function for unknown incoming commands
    # @return None
    def init(self, ip_address=None, ip_port=None, logger=None, verbose=None, callback=None):
        services.cfg = Cfg()
        if logger is not None:
            services.logger = logger
        if verbose is not None:
            services.cfg.verbose = verbose
        if ip_address is not None:
            services.cfg.ip_address = ip_address
        if ip_port is not None:
            services.cfg.ip_port = ip_port
        if callback is not None:
            services.cfg.callback = callback

        services.server.init()
        self._window = None
        self._menu = None
        self._screen = None

    # --------------------
    ## set the TK root window
    #
    # @param window   the TK root window
    # @return None
    def set_window(self, window):
        self._window = window

    # --------------------
    ## set the top level menu
    #
    # @param menu  the top level menu
    # @return None
    def set_menu(self, menu):
        self._menu = menu

    # --------------------
    ## in the given widget, set an internal name to be used for screen dump purposes
    #
    # @param widget  the widget to set the name in
    # @param name    the name to use
    # @return None
    def set_name(self, widget, name):
        setattr(widget, 'guiapi_name', name)

    # --------------------
    ## generate a left mouse button click at the given screen coordinates
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def click_left(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        services.logger.info(f'click_left: {x} {y}')
        win = self._window.winfo_containing(x, y)
        # uncomment to debug
        # n = getattr(w, 'guiapi_name', '<unknown>')
        # services.logger.info(f'DBG click_left: on widget.name: {n}')
        win.event_generate('<Enter>', x=x, y=y)
        win.event_generate('<Button-1>', x=x, y=y)
        win.event_generate('<ButtonRelease-1>', x=x, y=y)

        return rsp

    # --------------------
    ## set the text in the Entry widget
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def set_text(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        services.logger.info(f'set_text: {x} {y}')
        win = self._window.winfo_containing(x, y)
        # uncomment to debug
        # n = getattr(w, 'guiapi_name', '<unknown>')
        # services.logger.info(f'DBG set_text: on widget.name: {n}')

        # TODO confirm it is an Entry class
        # mvc.logger.info(f'DBG {w.winfo_class()}')
        # rsp['value'] = 'nak'
        # rsp['reason'] = 'must be an Entry widget'

        # send a keypress for each character in the incoming string
        win.focus_set()
        for ch in cmd['msg']:
            win.event_generate(f'<KeyPress-{ch}>')
        win.update()

        return rsp

    # --------------------
    ## get a screen dump in JSON format of the currently displayed screen(s)
    #
    # @return screen content in JSON format
    def get_screen(self):
        services.logger.info('get_screen')
        self._screen = self._report_window(self._window)

        # services.logger.info(f'screen:\n{json.dumps(self._screen, indent=4)}')
        services.logger.info('get_screen done')
        return self._screen

    # --------------------
    ## get screen content for the given window in JSON format
    #
    # @param win  the window to get the screen content for
    # @return screen content in JSON format
    def _report_window(self, win):
        node = {
            'class': win.winfo_class(),
            'name': getattr(win, 'guiapi_name', '<unknown>'),
            'title': win.title(),
            'geometry': win.geometry(),
        }
        self._get_coordinates(win, node)

        node['children'] = []
        for frame in win.winfo_children():
            child = {}
            self._report_child(frame, child)
            node['children'].append(child)

        return node

    # --------------------
    ## get screen content for the given frame in JSON format
    #
    # @param frame  the frame to get the screen content for
    # @param node   the node/widget to get the screen content for
    # @return screen content in JSON format
    def _report_child(self, frame, node):
        node['class'] = frame.winfo_class()
        node['name'] = getattr(frame, 'guiapi_name', '<unknown>')

        # menus are handled differently
        if frame.winfo_class() in ['Menu']:
            node['menu'] = []
            for index in range(0, frame.index('end') + 1):
                if frame.type(index) in ['command', 'cascade']:
                    menuitem = {
                        'index': index,
                        'type': frame.type(index),
                        'label': frame.entrycget(index, 'label'),
                        'state': frame.entrycget(index, 'state'),
                    }
                    node['menu'].append(menuitem)
        else:
            # text on the screen and the current enable/disable state
            if frame.winfo_class() in ['Label', 'Button', 'Radiobutton']:
                node['value'] = frame.cget('text')
                node['state'] = frame.cget('state')
            elif frame.winfo_class() in ['Listbox']:
                # value is a list of all possible items in the listbox
                node['value'] = frame.get(0, frame.index('end'))
                node['state'] = frame.cget('state')
            elif frame.winfo_class() in ['Entry']:
                node['value'] = frame.get()
                node['state'] = frame.cget('state')
            else:
                node['value'] = '<unknown>'
                node['state'] = '<unknown>'

        self._get_coordinates(frame, node)

        node['children'] = []
        for ch in frame.winfo_children():
            child = {}
            self._report_child(ch, child)
            node['children'].append(child)

    # --------------------
    ## get coordinates for the given widget and add it to the current node
    #
    # @param frame  the frame/widget to get the screen content for
    # @param node  the node to add the coordinates to
    # @return None
    def _get_coordinates(self, frame, node):
        x1 = frame.winfo_rootx()
        y1 = frame.winfo_rooty()
        x2 = x1 + frame.winfo_width()
        y2 = y1 + frame.winfo_height()
        node['coordinates'] = {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }

    # --------------------
    ## invoke a menu item with the given menu path
    #
    # @param cmd   a list of menu indicies to locate the menu item
    # @return ack/nak response in JSON format
    def menu_invoke(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        item = self._menu
        ok = False
        # uncomment to debug
        # services.logger.info(f'DBG guiapi {cmd["menu_path"]}')
        for index in cmd['menu_path']:
            # uncomment to debug
            # services.logger.info(f'DBG guiapi item:{item.index("end")}')
            if index <= item.index('end') and index == cmd['menu_path'][-1]:
                services.logger.info(f'DBG guiapi invoke {index} {cmd["menu_path"][-1]}')
                # this index is the last one in the menu_path so invoke it
                item.invoke(index)
                ok = True
                break

            # uncomment to debug
            # services.logger.info(f'DBG guiapi getting children')

            # check the children
            children = item.winfo_children()
            if len(children) >= 1:
                item = item.winfo_children()[0]
            else:
                break

        if not ok:
            rsp['value'] = 'nak'
            rsp['reason'] = 'menuitem not found'

        # uncoment to debug
        # services.logger.info(f'DBG guiapi exiting: {rsp}')
        return rsp

    # --------------------
    ## select an option on a listbox
    #
    # @param cmd   the incoming JSON command
    # @return ack/nak response in JSON format
    def lbox_select(self, cmd):
        rsp = {
            'rsp': cmd['cmd'],
            'value': 'ack',
        }

        x = cmd['x']
        y = cmd['y']
        services.logger.info(f'lbox_select: {x} {y}')
        win = self._window.winfo_containing(x, y)
        # uncomment to debug
        # n = getattr(w, 'guiapi_name', '<unknown>')
        # services.logger.info(f'DBG lbox_select: on widget.name: {n}')
        # w.selection_clear(0, tkinter.END)
        services.logger.info(f'lbox_select: current select: {win.curselection()}')
        win.selection_clear(0, 'end')
        for i in cmd['opt_id']:
            win.select_set(i)
        win.event_generate('<<ListboxSelect>>')

        return rsp
