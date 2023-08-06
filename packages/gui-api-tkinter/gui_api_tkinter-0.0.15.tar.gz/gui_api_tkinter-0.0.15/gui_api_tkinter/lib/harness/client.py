import json
import time

from socket_oneline import OnelineClient

from .. import services


# --------------------
## sample Client that wraps the OnelineClient
class Client:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to Oneline Client
        self._olclient = OnelineClient()

    # --------------------
    ## initialize the OnelineClient and connect to the server
    #
    # @return None
    def init(self):
        services.logger.info('client      : started')

        self._olclient.ip_address = services.cfg.ip_address
        self._olclient.ip_port = services.cfg.ip_port
        self._olclient.logger = services.logger
        self._olclient.verbose = False
        if not self._olclient.init():
            services.logger.info('ERR failed to set params')
            return

        self._olclient.connect()
        # TODO replace with wait_until... with timeout
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._olclient is not None:
            self._olclient.disconnect()
            self._olclient = None

    # --------------------
    ## ping the Server
    #
    # @return the response (should be 'pong')
    def is_connected(self) -> bool:
        # no json, this is a builtin command to OnelineClient
        self._olclient.send('ping')
        rsp = self._olclient.recv()
        return rsp == 'pong'

    # --------------------
    ## get screen content
    #
    # @return the response
    def get_screen(self):
        cmd = {
            'cmd': 'get_screen'
        }
        screen = self.send_recv(cmd)
        return screen

    # --------------------
    ## click left mouse button at given screen coordinates
    #
    # @param x  the x value in screen coordinates
    # @param y  the y value in screen coordinates
    # @return the response
    def click_left(self, x, y):
        cmd = {
            'cmd': 'click_left',
            'x': x,
            'y': y,
        }
        ack_nak = self.send_recv(cmd)
        # uncomment to debug
        # print(f'DBG client: cmd={json.dumps(cmd, indent=4)}\nrsp={json.dumps(ack_nak, indent=4)}')
        return ack_nak

    # --------------------
    ## select menu in the given menu path
    #
    # @param menu_path  a list of indicies indicating the menu path
    # @return the response
    def menu_click(self, menu_path):
        cmd = {
            'cmd': 'menu_click',
            'menu_path': menu_path,
        }
        ack_nak = self.send_recv(cmd)
        # uncomment to debug
        # print(f'DBG client: cmd={json.dumps(cmd, indent=4)}\nrsp={json.dumps(ack_nak, indent=4)}')
        return ack_nak

    # --------------------
    ## set text in an Entry widget
    #
    # @param x     the x coordinate of the widget to set text in
    # @param y     the y coordinate of the widget to set text in
    # @param text  the text to set
    # @return the response
    def set_text(self, x, y, text):
        cmd = {
            'cmd': 'set_text',
            'x': x,
            'y': y,
            'msg': text,
        }

        ack_nak = self.send_recv(cmd)
        # uncomment to debug
        # print(f'DBG client: cmd={json.dumps(cmd, indent=4)}\nrsp={json.dumps(ack_nak, indent=4)}')
        return ack_nak

    # --------------------
    ## select option in a Listbox widget
    #
    # @param x        the x coordinate of the widget
    # @param y        the y coordinate of the widget
    # @param opt_id   the option id to select
    # @return the response
    def lbox_select(self, x: int, y: int, opt_id: list):
        cmd = {
            'cmd': 'lbox_select',
            'x': x,
            'y': y,
            'opt_id': opt_id,
        }

        ack_nak = self.send_recv(cmd)
        # uncomment to debug
        # print(f'DBG client: cmd={json.dumps(cmd, indent=4)}\nrsp={json.dumps(ack_nak, indent=4)}')
        return ack_nak

    # --------------------
    ## send a command to the Server, wait for a response
    #
    # @param cmd  the command to send
    # @return the response
    def send_recv(self, cmd: dict) -> dict:
        self._send(cmd)
        return self._recv()

    # === Private

    # --------------------
    ## send a command to the Server
    #
    # @param cmd  the command to send
    # @return None
    def _send(self, cmd: dict):
        services.logger.info(f'client      : tx: {cmd}')
        cmdstr = json.dumps(cmd)
        self._olclient.send(cmdstr)

    # --------------------
    ## wait for a response from the Server
    #
    # @return the response
    def _recv(self) -> dict:
        rspstr = self._olclient.recv()
        rsp = json.loads(rspstr)
        # uncomment for debugging
        # services.logger.info(f'client      : rx: {rsp}')
        return rsp
